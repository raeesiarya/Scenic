from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


if __package__ in (None, ""):
    if str(Path(__file__).resolve().parent) not in sys.path:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
    from scenic_composition_analysis_helpers import (
        CompositionGraph,
        CompositionStatement,
        GraphEdge,
        GraphNode,
        Container,
        ExecutionStructure,
        SXOStructure,
        SXONode,
        SxOEdge,
        extract_from_parser,
        load_source,
        sort_node_ids,
        ordered_compositions,
        sample_composition,
    )
else:
    from .scenic_composition_analysis_helpers import (
        CompositionGraph,
        CompositionStatement,
        GraphEdge,
        GraphNode,
        Container,
        ExecutionStructure,
        SXOStructure,
        SXONode,
        SxOEdge,
        extract_from_parser,
        load_source,
        sort_node_ids,
        ordered_compositions,
        sample_composition,
    )


def build_graph(
    source_path: Optional[Path],
    source_kind: str,
    containers: Sequence[Container],
    statements: Sequence[CompositionStatement],
) -> CompositionGraph:
    """Build a composition graph from the extracted containers and composition statements.

    Args:
        source_path (Optional[Path]): The path to the source file.
        source_kind (str): The kind of the source.
        containers (Sequence[Container]): The list of containers.
        statements (Sequence[CompositionStatement]): The list of composition statements.

    Returns:
        CompositionGraph: The built composition graph.
    """
    nodes: List[GraphNode] = []
    edges: List[GraphEdge] = []
    container_ids = {}

    for container in containers:
        node_id = f"{container.kind}:{container.name}"
        container_ids[container.name] = node_id
        nodes.append(
            GraphNode(
                id=node_id,
                kind=container.kind,
                label=container.name,
                attributes={"name": container.name, "kind": container.kind},
            )
        )

    byContainer: Dict[str, List[CompositionStatement]] = {}
    for statement in statements:
        byContainer.setdefault(statement.container_name, []).append(statement)
        nodes.append(
            GraphNode(
                id=statement.node_id,
                kind="composition",
                label=statement.operator,
                attributes={
                    "container": statement.container_name,
                    "line": statement.line,
                    "nesting": list(statement.nesting),
                    **statement.semantics,
                },
            )
        )
        edges.append(
            GraphEdge(
                source=container_ids[statement.container_name],
                target=statement.node_id,
                kind="contains",
                attributes={"line": statement.line},
            )
        )
        for index, invocation in enumerate(statement.invocations):
            inv_id = f"{statement.node_id}:invocation:{index}"
            nodes.append(
                GraphNode(
                    id=inv_id,
                    kind="invocation",
                    label=invocation.target or invocation.text,
                    attributes=asdict(invocation),
                )
            )
            edges.append(
                GraphEdge(
                    source=statement.node_id,
                    target=inv_id,
                    kind="invokes",
                    attributes={"weight": invocation.weight},
                )
            )

    for container_name, container_statements in byContainer.items():
        ordered = sorted(container_statements, key=lambda stmt: stmt.line or -1)
        for left, right in zip(ordered, ordered[1:]):
            edges.append(
                GraphEdge(
                    source=left.node_id,
                    target=right.node_id,
                    kind="next",
                    attributes={"within": container_name},
                )
            )

    return CompositionGraph(
        source_path=str(source_path) if source_path else None,
        source_kind=source_kind,
        container_names=tuple(container.name for container in containers),
        statements=tuple(statements),
        nodes=tuple(nodes),
        edges=tuple(edges),
    )


def analyze_scenic_composition(source: Union[str, Path]) -> CompositionGraph:
    """Analyze the composition structure of a Scenic source.

    Args:
        source (Union[str, Path]): The Scenic source to analyze.

    Returns:
        CompositionGraph: The analyzed composition graph.
    """
    text, source_path, source_kind = load_source(source)
    containers, statements = _extract_recursive(text, source_path)

    return build_graph(
        source_path=source_path,
        source_kind=source_kind,
        containers=containers,
        statements=statements,
    )


def find_composition_statements(
    source: Union[str, Path],
) -> Tuple[CompositionStatement, ...]:
    """Find all composition statements in a Scenic source.

    Args:
        source (Union[str, Path]): The Scenic source to analyze.

    Returns:
        Tuple[CompositionStatement, ...]: The list of composition statements.
    """
    return analyze_scenic_composition(source).statements


def _extract_recursive(
    text: str,
    source_path: Optional[Path],
    visited: Optional[set[Path]] = None,
) -> Tuple[List[Container], List[CompositionStatement]]:
    """Extract local containers/statements and merge in local Scenic-file dependencies."""

    containers, statements = extract_from_parser(text)
    if source_path is None:
        return containers, statements

    if visited is None:
        visited = set()
    resolved_path = source_path.resolve()
    if resolved_path in visited:
        return [], []
    visited.add(resolved_path)

    merged_containers = list(containers)
    merged_statements = list(statements)
    seen_containers = {(container.kind, container.name) for container in containers}

    for dependency_path in _find_local_scenic_dependencies(text, resolved_path):
        dep_text, _, _ = load_source(dependency_path)
        dep_containers, dep_statements = _extract_recursive(
            dep_text, dependency_path, visited
        )
        for container in dep_containers:
            if container.name == "<initial>":
                continue
            key = (container.kind, container.name)
            if key in seen_containers:
                continue
            seen_containers.add(key)
            merged_containers.append(container)
        imported_statement_ids = {statement.node_id for statement in merged_statements}
        for statement in dep_statements:
            if statement.node_id not in imported_statement_ids:
                merged_statements.append(statement)

    return merged_containers, merged_statements


def _find_local_scenic_dependencies(text: str, source_path: Path) -> List[Path]:
    """Resolve local Scenic imports such as `from helper import *` or `from . import sub`."""

    dependency_paths: List[Path] = []
    seen_paths = set()
    source_dir = source_path.parent

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        import_match = re.match(r"^from\s+([.\w]+)\s+import\b", line)
        if import_match:
            module_name = import_match.group(1)
            candidate = _resolve_local_scenic_module(module_name, source_dir)
            if candidate is not None and candidate not in seen_paths:
                seen_paths.add(candidate)
                dependency_paths.append(candidate)
            continue

        module_match = re.match(r"^import\s+([A-Za-z_][\w]*)\s*$", line)
        if module_match:
            candidate = source_dir / f"{module_match.group(1)}.scenic"
            if candidate.exists():
                candidate = candidate.resolve()
                if candidate not in seen_paths:
                    seen_paths.add(candidate)
                    dependency_paths.append(candidate)

    return dependency_paths


def _resolve_local_scenic_module(module_name: str, source_dir: Path) -> Optional[Path]:
    """Resolve a Scenic module reference to a local `.scenic` file when possible."""

    if module_name.startswith("scenic."):
        return None
    if module_name == "scenic":
        return None

    if module_name.startswith("."):
        relative_depth = len(module_name) - len(module_name.lstrip("."))
        remainder = module_name[relative_depth:]
        base_dir = source_dir
        for _ in range(max(relative_depth - 1, 0)):
            base_dir = base_dir.parent
        if not remainder:
            return None
        candidate = base_dir.joinpath(*remainder.split(".")).with_suffix(".scenic")
        return candidate.resolve() if candidate.exists() else None

    candidate = source_dir.joinpath(*module_name.split(".")).with_suffix(".scenic")
    return candidate.resolve() if candidate.exists() else None


def build_execution_structure(graph: CompositionGraph) -> ExecutionStructure:
    """Build an execution structure from the composition graph, organizing containers, compositions, and invocations in a way that reflects the execution semantics of the composition graph.

    Args:
        graph (CompositionGraph): The composition graph to convert.

    Returns:
        ExecutionStructure: The execution structure.
    """

    node_by_id = {node.id: node for node in graph.nodes}
    contains_by_container: Dict[str, List[str]] = {}
    invokes_by_composition: Dict[str, List[str]] = {}
    next_by_composition: Dict[str, List[str]] = {}
    incoming_next: Dict[str, int] = {}

    for edge in graph.edges:
        if edge.kind == "contains":
            contains_by_container.setdefault(edge.source, []).append(edge.target)
        elif edge.kind == "invokes":
            invokes_by_composition.setdefault(edge.source, []).append(edge.target)
        elif edge.kind == "next":
            next_by_composition.setdefault(edge.source, []).append(edge.target)
            incoming_next[edge.target] = incoming_next.get(edge.target, 0) + 1

    containers: Dict[str, Dict[str, Any]] = {}
    container_ids: List[str] = []
    for node in graph.nodes:
        if node.kind not in {"initial", "scenario", "behavior"}:
            continue
        container_ids.append(node.id)
        composition_ids = sort_node_ids(
            contains_by_container.get(node.id, []), node_by_id
        )
        start_ids = sort_node_ids(
            [
                node_id
                for node_id in composition_ids
                if incoming_next.get(node_id, 0) == 0
            ],
            node_by_id,
        )
        containers[node.id] = {
            "node": node,
            "composition_ids": composition_ids,
            "start_ids": start_ids,
        }

    compositions: Dict[str, Dict[str, Any]] = {}
    for node in graph.nodes:
        if node.kind != "composition":
            continue
        compositions[node.id] = {
            "node": node,
            "invocation_ids": sort_node_ids(
                invokes_by_composition.get(node.id, []), node_by_id
            ),
            "next_ids": sort_node_ids(next_by_composition.get(node.id, []), node_by_id),
        }

    invocations = {node.id: node for node in graph.nodes if node.kind == "invocation"}

    return ExecutionStructure(
        container_ids=tuple(container_ids),
        containers=containers,
        compositions=compositions,
        invocations=invocations,
        node_by_id=node_by_id,
    )


def build_sxo_structure(graph: CompositionGraph) -> SXOStructure:
    """Build an SxO structure from the composition graph, where scenarios and behaviors are represented as S nodes, compositions as X nodes, and invocations as O nodes. Edges represent the relationships between these nodes based on the "contains", "invokes", and "next" edges in the composition graph, as well as additional edges from invocations to their target containers.

    Args:
        graph (CompositionGraph): The composition graph to convert.

    Returns:
        SXOStructure: The simplified composition graph structure.
    """

    sxo_nodes: List[SXONode] = []
    sxo_edges: List[SxOEdge] = []
    container_name_to_s_id: Dict[str, str] = {}

    for node in graph.nodes:
        if node.kind in {"initial", "scenario", "behavior"}:
            s_id = f"S:{node.id}"
            container_name_to_s_id[node.label] = s_id
            sxo_nodes.append(
                SXONode(
                    id=s_id,
                    kind="S",
                    label=node.label,
                    attributes={"container_kind": node.kind, **node.attributes},
                )
            )
        elif node.kind == "composition":
            sxo_nodes.append(
                SXONode(
                    id=f"X:{node.id}",
                    kind="X",
                    label=node.label,
                    attributes=dict(node.attributes),
                )
            )
        elif node.kind == "invocation":
            sxo_nodes.append(
                SXONode(
                    id=f"O:{node.id}",
                    kind="O",
                    label=node.label,
                    attributes=dict(node.attributes),
                )
            )

    for edge in graph.edges:
        if edge.kind == "contains":
            sxo_edges.append(
                SxOEdge(
                    source=f"S:{edge.source}",
                    target=f"X:{edge.target}",
                    kind="S_to_X",
                    attributes=dict(edge.attributes),
                )
            )
        elif edge.kind == "invokes":
            sxo_edges.append(
                SxOEdge(
                    source=f"X:{edge.source}",
                    target=f"O:{edge.target}",
                    kind="X_to_O",
                    attributes=dict(edge.attributes),
                )
            )
        elif edge.kind == "next":
            sxo_edges.append(
                SxOEdge(
                    source=f"X:{edge.source}",
                    target=f"X:{edge.target}",
                    kind="X_to_X",
                    attributes=dict(edge.attributes),
                )
            )

    for node in graph.nodes:
        if node.kind != "invocation":
            continue
        target = node.attributes.get("target")
        if target in container_name_to_s_id:
            sxo_edges.append(
                SxOEdge(
                    source=f"O:{node.id}",
                    target=container_name_to_s_id[target],
                    kind="O_targets_S",
                    attributes={},
                )
            )

    return SXOStructure(nodes=tuple(sxo_nodes), edges=tuple(sxo_edges))


def _choice_probabilities(
    invocation_ids: Sequence[str], sxo: SXOStructure
) -> Dict[str, float]:
    """Compute normalized probabilities for a choice node's outgoing O nodes."""

    node_by_id = {node.id: node for node in sxo.nodes}
    weights = [
        node_by_id[node_id].attributes.get("weight") for node_id in invocation_ids
    ]
    if any(weight is not None for weight in weights):
        numeric_weights = [float(weight or 0.0) for weight in weights]
        total = sum(numeric_weights)
        if total > 0:
            return {
                node_id: weight / total
                for node_id, weight in zip(invocation_ids, numeric_weights)
            }
    if not invocation_ids:
        return {}
    uniform = 1.0 / len(invocation_ids)
    return {node_id: uniform for node_id in invocation_ids}


def build_compact_graph_dict(graph: CompositionGraph) -> Dict[str, Any]:
    """Build a compact dictionary export of the S/X/O graph for downstream consumers."""

    sxo = build_sxo_structure(graph)
    node_by_id = {node.id: node for node in sxo.nodes}
    compact_nodes: Dict[str, Dict[str, Any]] = {}

    for node in sxo.nodes:
        if node.kind == "S":
            compact_nodes[node.id] = {
                "type": "S",
                "name": node.label,
                "container_kind": node.attributes.get("container_kind"),
            }
        elif node.kind == "X":
            compact_nodes[node.id] = {
                "type": "X",
                "op": node.label,
                "container": node.attributes.get("container"),
            }
        elif node.kind == "O":
            compact_nodes[node.id] = {
                "type": "O",
                "target": node.attributes.get("target") or node.label,
            }

    compact_edges: List[Dict[str, Any]] = []
    outgoing_o_by_x: Dict[str, List[str]] = {}
    for edge in sxo.edges:
        if edge.kind == "X_to_O":
            outgoing_o_by_x.setdefault(edge.source, []).append(edge.target)

    for edge in sxo.edges:
        compact_edge = {
            "source": edge.source,
            "target": edge.target,
            "type": edge.kind,
        }
        if edge.kind == "X_to_O":
            source_node = node_by_id[edge.source]
            target_node = node_by_id[edge.target]
            weight = target_node.attributes.get("weight")
            if weight is not None:
                compact_edge["weight"] = weight
            if source_node.label == "choose":
                probabilities = _choice_probabilities(
                    outgoing_o_by_x.get(edge.source, []), sxo
                )
                if edge.target in probabilities:
                    compact_edge["probability"] = probabilities[edge.target]
        compact_edges.append(compact_edge)

    return {
        "nodes": compact_nodes,
        "edges": compact_edges,
    }


def _execution_choice_probabilities(
    invocation_ids: Sequence[str], invocation_nodes: Dict[str, GraphNode]
) -> Dict[str, float]:
    """Compute normalized probabilities for execution invocations."""

    weights = [
        invocation_nodes[node_id].attributes.get("weight") for node_id in invocation_ids
    ]
    if any(weight is not None for weight in weights):
        numeric_weights = [
            float(weight if weight is not None else 1.0) for weight in weights
        ]
        total = sum(numeric_weights)
        if total > 0:
            return {
                node_id: weight / total
                for node_id, weight in zip(invocation_ids, numeric_weights)
            }
    if not invocation_ids:
        return {}
    uniform = 1.0 / len(invocation_ids)
    return {node_id: uniform for node_id in invocation_ids}


def build_partner_format(graph: CompositionGraph) -> Dict[str, Any]:
    """Build a lightweight partner-facing container/steps export.

    Each container is represented as a sequence of steps where:
    - deterministic steps are plain strings
    - choose steps are bare probability dictionaries
    - shuffle steps are structured dictionaries to preserve operator meaning
    """

    execution = build_execution_structure(graph)
    container_id_by_name = {
        container["node"].label: container_id
        for container_id, container in execution.containers.items()
    }
    referenced_container_names = {
        invocation.attributes.get("target")
        for invocation in execution.invocations.values()
        if invocation.attributes.get("target") in container_id_by_name
    }
    entrypoints = [
        execution.containers[container_id]["node"].label
        for container_id in execution.container_ids
        if execution.containers[container_id]["node"].kind in {"scenario", "behavior"}
        and execution.containers[container_id]["node"].label
        not in referenced_container_names
    ]
    if not entrypoints:
        entrypoints = [
            execution.containers[container_id]["node"].label
            for container_id in execution.container_ids
            if execution.containers[container_id]["node"].kind
            in {"scenario", "behavior"}
        ]

    containers: Dict[str, Dict[str, Any]] = {}
    for container_id in execution.container_ids:
        container = execution.containers[container_id]
        node = container["node"]
        if node.kind not in {"scenario", "behavior"}:
            continue

        steps: List[Any] = []
        for composition_id in ordered_compositions(container, execution):
            composition = execution.compositions[composition_id]
            operator = composition["node"].label
            invocation_ids = list(composition["invocation_ids"])
            labels = [
                execution.invocations[invocation_id].attributes.get("target")
                or execution.invocations[invocation_id].attributes["text"]
                for invocation_id in invocation_ids
            ]

            if operator in {"parallel", "until", "for"}:
                steps.extend(labels)
            elif operator == "choose":
                probabilities = _execution_choice_probabilities(
                    invocation_ids, execution.invocations
                )
                steps.append(
                    {
                        label: probabilities[invocation_id]
                        for invocation_id, label in zip(invocation_ids, labels)
                    }
                )
            elif operator == "shuffle":
                probabilities = _execution_choice_probabilities(
                    invocation_ids, execution.invocations
                )
                steps.append(
                    {
                        "shuffle": {
                            label: probabilities[invocation_id]
                            for invocation_id, label in zip(invocation_ids, labels)
                        }
                    }
                )

        containers[node.label] = {
            "kind": node.kind,
            "steps": steps,
        }

    return {
        "entrypoints": entrypoints,
        "containers": containers,
    }


def sample_from_graph(graph: CompositionGraph) -> List[str]:
    """Sample a possible execution trace from the composition graph by traversing the execution structure and making random choices at composition and invocation nodes.

    Args:
        graph (CompositionGraph): The composition graph to sample from.

    Returns:
        List[str]: A sample execution trace based on the composition structure of the graph.
    """

    execution = build_execution_structure(graph)
    container_id_by_name = {
        container["node"].label: container_id
        for container_id, container in execution.containers.items()
    }
    referenced_container_names = {
        invocation.attributes.get("target")
        for invocation in execution.invocations.values()
        if invocation.attributes.get("target") in container_id_by_name
    }

    entry_container_ids = [
        container_id
        for container_id in execution.container_ids
        if execution.containers[container_id]["node"].kind in {"scenario", "behavior"}
        and execution.containers[container_id]["node"].label
        not in referenced_container_names
    ]
    if not entry_container_ids:
        entry_container_ids = [
            container_id
            for container_id in execution.container_ids
            if execution.containers[container_id]["node"].kind
            in {"scenario", "behavior"}
        ]

    trace: List[str] = []
    for container_id in entry_container_ids:
        trace.extend(
            _sample_container_recursive(
                container_id, execution, container_id_by_name, active_containers=set()
            )
        )

    return trace


def _sample_container_recursive(
    container_id: str,
    execution: ExecutionStructure,
    container_id_by_name: Dict[str, str],
    active_containers: set[str],
) -> List[str]:
    """Sample a container and recursively follow invoked container targets."""

    if container_id in active_containers:
        return []

    active_containers = set(active_containers)
    active_containers.add(container_id)
    trace: List[str] = []
    container = execution.containers[container_id]

    for composition_id in ordered_compositions(container, execution):
        sampled_targets = sample_composition(
            execution.compositions[composition_id], execution.invocations
        )
        trace.extend(sampled_targets)
        for target in sampled_targets:
            target_container_id = container_id_by_name.get(target)
            if target_container_id is None:
                continue
            trace.extend(
                _sample_container_recursive(
                    target_container_id,
                    execution,
                    container_id_by_name,
                    active_containers,
                )
            )

    return trace


def run_scenic_composition(source: Union[str, Path]) -> List[str]:
    """Run the composition structure of a Scenic source and return a sample execution trace.

    Args:
        source (Union[str, Path]): The Scenic source to run.

    Returns:
        List[str]: A sample execution trace based on the composition structure of the source.
    """

    graph = analyze_scenic_composition(source)
    return sample_from_graph(graph)


def build_analysis_output(source: Union[str, Path]) -> Dict[str, Any]:
    """Build the complete analysis payload printed by the CLI."""

    graph = analyze_scenic_composition(source)
    execution = build_execution_structure(graph)
    sxo = build_sxo_structure(graph)
    compact = build_compact_graph_dict(graph)
    partner = build_partner_format(graph)
    sample = sample_from_graph(graph)

    return {
        "graph": graph.as_dict(),
        "execution_structure": execution.as_dict(),
        "sxo_structure": sxo.as_dict(),
        "compact_graph": compact,
        "partner_format": partner,
        "sample_trace": sample,
    }


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(
            "usage: python tools/scenic_composition_analysis.py <scenic-file>"
        )
    graph = analyze_scenic_composition(sys.argv[1])
    print(json.dumps(build_partner_format(graph), indent=2))
