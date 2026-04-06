from pathlib import Path

import pytest

from tools.scenic_composition_analysis import (
    analyze_scenic_composition,
    build_execution_structure,
    build_compact_graph_dict,
    build_analysis_output,
    build_partner_format,
    build_sxo_structure,
    find_composition_statements,
    sample_from_graph,
)

SCENIC_TEST_MAIN = "examples/scenic_tests/cases_simple/case_interconnected/main.scenic"
SCENIC_TEST_STRAIGHT = "examples/scenic_tests/cases_simple/case_straight/main.scenic"
SCENIC_TEST_SCENARIO = "examples/scenic_tests/cases_simple/case_scenario/main.scenic"
SCENIC_TEST_INTERRUPT = (
    "examples/scenic_tests/cases_simple/case_interrupt_temporal/main.scenic"
)
SCENIC_TEST_MONITOR = (
    "examples/scenic_tests/cases_simple/case_monitor_require/main.scenic"
)
SCENIC_TEST_WEIGHTED_SHUFFLE = (
    "examples/scenic_tests/cases_simple/case_weighted_shuffle/main.scenic"
)
REALISTIC_CASES = [
    "examples/scenic_tests/cases_realistic/black_ice_ramp/main.scenic",
    "examples/scenic_tests/cases_realistic/broken_lights_intersection/main.scenic",
    "examples/scenic_tests/cases_realistic/child_darting/main.scenic",
    "examples/scenic_tests/cases_realistic/debris_cascade/main.scenic",
    "examples/scenic_tests/cases_realistic/emergency_merge/main.scenic",
    "examples/scenic_tests/cases_realistic/jackknife_rain/main.scenic",
    "examples/scenic_tests/cases_realistic/pileup_fog/main.scenic",
    "examples/scenic_tests/cases_realistic/tunnel_exit_glare/main.scenic",
    "examples/scenic_tests/cases_realistic/urban_conflict/main.scenic",
    "examples/scenic_tests/cases_realistic/wrong_way_freeway/main.scenic",
]


GRAPH_CASES = [
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_03.scenic",
        "containers": ("<initial>", "CollisionAvoidance", "FollowLeadCarBehavior"),
        "statement_containers": ("FollowLeadCarBehavior", "FollowLeadCarBehavior"),
        "statement_node_ids": ("FollowLeadCarBehavior:1", "FollowLeadCarBehavior:2"),
        "invocation_texts": ("FollowLaneBehavior()", "CollisionAvoidance()"),
        "invocation_targets": ("FollowLaneBehavior", "CollisionAvoidance"),
        "nestings": (
            ("try",),
            ("try", "interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE)"),
        ),
        "node_counts": {"initial": 1, "behavior": 2, "composition": 2, "invocation": 2},
        "edge_counts": {"contains": 2, "invokes": 2, "next": 1},
        "next_within": ("FollowLeadCarBehavior",),
        "non_composition_containers": ("<initial>", "CollisionAvoidance"),
    },
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_04.scenic",
        "containers": (
            "<initial>",
            "LeadCarBehavior",
            "CollisionAvoidance",
            "FollowLeadCarBehavior",
        ),
        "statement_containers": (
            "LeadCarBehavior",
            "FollowLeadCarBehavior",
            "FollowLeadCarBehavior",
        ),
        "statement_node_ids": (
            "LeadCarBehavior:1",
            "FollowLeadCarBehavior:1",
            "FollowLeadCarBehavior:2",
        ),
        "invocation_texts": (
            "FollowLaneBehavior()",
            "FollowLaneBehavior()",
            "CollisionAvoidance()",
        ),
        "invocation_targets": (
            "FollowLaneBehavior",
            "FollowLaneBehavior",
            "CollisionAvoidance",
        ),
        "nestings": (
            ("try",),
            ("try",),
            ("try", "interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE)"),
        ),
        "node_counts": {"initial": 1, "behavior": 3, "composition": 3, "invocation": 3},
        "edge_counts": {"contains": 3, "invokes": 3, "next": 1},
        "next_within": ("FollowLeadCarBehavior",),
        "non_composition_containers": ("<initial>", "CollisionAvoidance"),
    },
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_28.scenic",
        "containers": ("<initial>", "EgoBehavior", "OtherCarBehavior"),
        "statement_containers": ("EgoBehavior", "OtherCarBehavior"),
        "statement_node_ids": ("EgoBehavior:1", "OtherCarBehavior:1"),
        "invocation_texts": (
            "FollowTrajectoryBehavior(target_speed=target_speed, trajectory=trajectory)",
            "FollowTrajectoryBehavior(target_speed=8, trajectory=trajectory)",
        ),
        "invocation_targets": ("FollowTrajectoryBehavior", "FollowTrajectoryBehavior"),
        "nestings": (("try",), ()),
        "node_counts": {"initial": 1, "behavior": 2, "composition": 2, "invocation": 2},
        "edge_counts": {"contains": 2, "invokes": 2, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_29.scenic",
        "containers": ("<initial>", "EgoBehavior"),
        "statement_containers": ("EgoBehavior",),
        "statement_node_ids": ("EgoBehavior:1",),
        "invocation_texts": (
            "FollowTrajectoryBehavior(target_speed=target_speed, trajectory=trajectory)",
        ),
        "invocation_targets": ("FollowTrajectoryBehavior",),
        "nestings": (("try",),),
        "node_counts": {"initial": 1, "behavior": 1, "composition": 1, "invocation": 1},
        "edge_counts": {"contains": 1, "invokes": 1, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_30.scenic",
        "containers": ("<initial>", "SafeBehavior", "EgoBehavior"),
        "statement_containers": ("SafeBehavior", "EgoBehavior"),
        "statement_node_ids": ("SafeBehavior:1", "EgoBehavior:1"),
        "invocation_texts": (
            "FollowTrajectoryBehavior(target_speed=target_speed, trajectory=trajectory)",
            "FollowTrajectoryBehavior(target_speed, trajectory)",
        ),
        "invocation_targets": ("FollowTrajectoryBehavior", "FollowTrajectoryBehavior"),
        "nestings": (("try",), ()),
        "node_counts": {"initial": 1, "behavior": 2, "composition": 2, "invocation": 2},
        "edge_counts": {"contains": 2, "invokes": 2, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
    {
        "path": "examples/driving/OAS_Scenarios/oas_scenario_32.scenic",
        "containers": ("<initial>", "FollowTrafficBehavior", "SafeBehavior"),
        "statement_containers": ("FollowTrafficBehavior", "SafeBehavior"),
        "statement_node_ids": ("FollowTrafficBehavior:1", "SafeBehavior:1"),
        "invocation_texts": (
            "FollowTrajectoryBehavior(target_speed, trajectory)",
            "FollowTrajectoryBehavior(target_speed=target_speed, trajectory=trajectory)",
        ),
        "invocation_targets": ("FollowTrajectoryBehavior", "FollowTrajectoryBehavior"),
        "nestings": ((), ("try",)),
        "node_counts": {"initial": 1, "behavior": 2, "composition": 2, "invocation": 2},
        "edge_counts": {"contains": 2, "invokes": 2, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
    {
        "path": "examples/driving/Carla_Challenge/carlaChallenge2.scenic",
        "containers": ("<initial>", "EgoBehavior", "LeadingCarBehavior"),
        "statement_containers": ("EgoBehavior", "LeadingCarBehavior"),
        "statement_node_ids": ("EgoBehavior:1", "LeadingCarBehavior:1"),
        "invocation_texts": ("FollowLaneBehavior(speed)", "FollowLaneBehavior(speed)"),
        "invocation_targets": ("FollowLaneBehavior", "FollowLaneBehavior"),
        "nestings": (("try",), ("try",)),
        "node_counts": {"initial": 1, "behavior": 2, "composition": 2, "invocation": 2},
        "edge_counts": {"contains": 2, "invokes": 2, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
    {
        "path": "examples/driving/Carla_Challenge/carlaChallenge3.scenic",
        "containers": ("<initial>", "EgoBehavior"),
        "statement_containers": ("EgoBehavior",),
        "statement_node_ids": ("EgoBehavior:1",),
        "invocation_texts": ("FollowLaneBehavior(speed)",),
        "invocation_targets": ("FollowLaneBehavior",),
        "nestings": (("try",),),
        "node_counts": {"initial": 1, "behavior": 1, "composition": 1, "invocation": 1},
        "edge_counts": {"contains": 1, "invokes": 1, "next": 0},
        "next_within": (),
        "non_composition_containers": ("<initial>",),
    },
]


def count_by_kind(items):
    counts = {}
    for item in items:
        counts[item.kind] = counts.get(item.kind, 0) + 1
    return counts


@pytest.mark.parametrize(
    "case", GRAPH_CASES, ids=[Path(case["path"]).stem for case in GRAPH_CASES]
)
def test_analyze_scenic_composition_builds_expected_graph_structure(case):
    graph = analyze_scenic_composition(case["path"])

    assert graph.source_kind == "path"
    assert graph.source_path == str(Path(case["path"]).resolve())
    assert graph.container_names == case["containers"]

    assert [statement.container_name for statement in graph.statements] == list(
        case["statement_containers"]
    )
    assert [statement.node_id for statement in graph.statements] == list(
        case["statement_node_ids"]
    )
    assert [statement.operator for statement in graph.statements] == ["parallel"] * len(
        case["statement_containers"]
    )
    assert [statement.invocations[0].text for statement in graph.statements] == list(
        case["invocation_texts"]
    )
    assert [statement.invocations[0].target for statement in graph.statements] == list(
        case["invocation_targets"]
    )
    assert [statement.nesting for statement in graph.statements] == list(
        case["nestings"]
    )

    node_counts = count_by_kind(graph.nodes)
    for kind, expected in case["node_counts"].items():
        assert node_counts.get(kind, 0) == expected

    edge_counts = count_by_kind(graph.edges)
    for kind, expected in case["edge_counts"].items():
        assert edge_counts.get(kind, 0) == expected

    next_edges = [edge for edge in graph.edges if edge.kind == "next"]
    assert (
        tuple(edge.attributes["within"] for edge in next_edges) == case["next_within"]
    )

    composition_node_ids = {
        node.id for node in graph.nodes if node.kind == "composition"
    }
    invocation_node_ids = {node.id for node in graph.nodes if node.kind == "invocation"}
    assert composition_node_ids == set(case["statement_node_ids"])
    assert invocation_node_ids == {
        f"{statement_id}:invocation:0" for statement_id in case["statement_node_ids"]
    }

    contains_edges = [edge for edge in graph.edges if edge.kind == "contains"]
    assert {(edge.source, edge.target) for edge in contains_edges} == {
        (f"behavior:{statement.container_name}", statement.node_id)
        for statement in graph.statements
    }

    invokes_edges = [edge for edge in graph.edges if edge.kind == "invokes"]
    assert {(edge.source, edge.target) for edge in invokes_edges} == {
        (statement.node_id, f"{statement.node_id}:invocation:0")
        for statement in graph.statements
    }

    containers_with_statements = {
        statement.container_name for statement in graph.statements
    }
    assert all(
        container_name not in containers_with_statements
        for container_name in case["non_composition_containers"]
    )

    node_ids = {node.id for node in graph.nodes}
    assert all(
        edge.source in node_ids and edge.target in node_ids for edge in graph.edges
    )


def test_oas03_graph_preserves_behavior_order_and_nesting():
    graph = analyze_scenic_composition(
        "examples/driving/OAS_Scenarios/oas_scenario_03.scenic"
    )

    assert len(graph.statements) == 2
    assert graph.statements[0].container_name == "FollowLeadCarBehavior"
    assert graph.statements[0].invocations[0].text == "FollowLaneBehavior()"
    assert graph.statements[0].nesting == ("try",)

    assert graph.statements[1].container_name == "FollowLeadCarBehavior"
    assert graph.statements[1].invocations[0].text == "CollisionAvoidance()"
    assert graph.statements[1].nesting == (
        "try",
        "interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE)",
    )


def test_oas04_graph_has_one_next_edge_only_within_follow_lead_behavior():
    graph = analyze_scenic_composition(
        "examples/driving/OAS_Scenarios/oas_scenario_04.scenic"
    )

    next_edges = [edge for edge in graph.edges if edge.kind == "next"]

    assert len(next_edges) == 1
    assert next_edges[0].source == "FollowLeadCarBehavior:1"
    assert next_edges[0].target == "FollowLeadCarBehavior:2"
    assert next_edges[0].attributes["within"] == "FollowLeadCarBehavior"


def test_find_composition_statements_matches_analyze_output_for_all_examples():
    for case in GRAPH_CASES:
        path = case["path"]
        graph = analyze_scenic_composition(path)
        statements = find_composition_statements(path)

        assert statements == graph.statements


@pytest.mark.parametrize(
    "case",
    GRAPH_CASES,
    ids=[f"{Path(case['path']).stem}-json" for case in GRAPH_CASES],
)
def test_graph_json_shape_matches_analysis_output_for_all_examples(case):
    graph = analyze_scenic_composition(case["path"])

    as_dict = graph.as_dict()

    assert as_dict["source_path"] == str(Path(case["path"]).resolve())
    assert as_dict["container_names"] == case["containers"]
    assert (
        tuple(stmt["container_name"] for stmt in as_dict["statements"])
        == case["statement_containers"]
    )
    assert (
        tuple(stmt["node_id"] for stmt in as_dict["statements"])
        == case["statement_node_ids"]
    )
    assert (
        tuple(stmt["invocations"][0]["text"] for stmt in as_dict["statements"])
        == case["invocation_texts"]
    )
    assert (
        tuple(stmt["invocations"][0]["target"] for stmt in as_dict["statements"])
        == case["invocation_targets"]
    )
    assert (
        tuple(node["kind"] for node in as_dict["nodes"]).count("composition")
        == case["node_counts"]["composition"]
    )
    assert (
        tuple(edge["kind"] for edge in as_dict["edges"]).count("contains")
        == case["edge_counts"]["contains"]
    )


def test_graph_json_shape_matches_analysis_output():
    graph = analyze_scenic_composition(
        "examples/driving/OAS_Scenarios/oas_scenario_29.scenic"
    )

    as_dict = graph.as_dict()

    assert as_dict["container_names"] == ("<initial>", "EgoBehavior")
    assert as_dict["statements"][0]["container_name"] == "EgoBehavior"
    assert as_dict["nodes"][0]["kind"] == "initial"
    assert {edge["kind"] for edge in as_dict["edges"]} == {"contains", "invokes"}


def test_build_compact_graph_dict_has_simple_sxo_shape():
    graph = analyze_scenic_composition(
        "examples/driving/OAS_Scenarios/oas_scenario_03.scenic"
    )

    compact = build_compact_graph_dict(graph)

    assert set(compact.keys()) == {"nodes", "edges"}
    assert compact["nodes"]["S:behavior:FollowLeadCarBehavior"] == {
        "type": "S",
        "name": "FollowLeadCarBehavior",
        "container_kind": "behavior",
    }
    assert compact["nodes"]["X:FollowLeadCarBehavior:1"] == {
        "type": "X",
        "op": "parallel",
        "container": "FollowLeadCarBehavior",
    }
    assert compact["nodes"]["O:FollowLeadCarBehavior:2:invocation:0"] == {
        "type": "O",
        "target": "CollisionAvoidance",
    }
    assert {"source", "target", "type"} <= set(compact["edges"][0].keys())
    assert {
        (edge["source"], edge["target"], edge["type"]) for edge in compact["edges"]
    } == {
        (
            "S:behavior:FollowLeadCarBehavior",
            "X:FollowLeadCarBehavior:1",
            "S_to_X",
        ),
        (
            "X:FollowLeadCarBehavior:1",
            "O:FollowLeadCarBehavior:1:invocation:0",
            "X_to_O",
        ),
        (
            "S:behavior:FollowLeadCarBehavior",
            "X:FollowLeadCarBehavior:2",
            "S_to_X",
        ),
        (
            "X:FollowLeadCarBehavior:2",
            "O:FollowLeadCarBehavior:2:invocation:0",
            "X_to_O",
        ),
        (
            "X:FollowLeadCarBehavior:1",
            "X:FollowLeadCarBehavior:2",
            "X_to_X",
        ),
        (
            "O:FollowLeadCarBehavior:2:invocation:0",
            "S:behavior:CollisionAvoidance",
            "O_targets_S",
        ),
    }


def test_build_compact_graph_dict_adds_uniform_probabilities_for_choose():
    graph = analyze_scenic_composition(
        "behavior MainBehavior():\n"
        "    do choose Foo(), Bar()\n"
    )

    compact = build_compact_graph_dict(graph)
    choose_edges = [
        edge
        for edge in compact["edges"]
        if edge["type"] == "X_to_O"
    ]

    assert len(choose_edges) == 2
    assert {edge["probability"] for edge in choose_edges} == {0.5}


def test_sample_from_graph_recurses_into_invoked_containers():
    graph = analyze_scenic_composition(
        "behavior MainBehavior():\n"
        "    do HelperBehavior()\n\n"
        "behavior HelperBehavior():\n"
        "    do LeafBehavior()\n"
    )

    assert sample_from_graph(graph) == ["HelperBehavior", "LeafBehavior"]


def test_main_scenic_builds_full_recursive_graph():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "LocalBranch",
        "LocalA",
        "LocalB",
        "LocalLeaf",
        "ShuffleTail",
        "TailA",
        "TailB",
        "ImportedBranch",
        "WeightedA",
        "Helper2Leaf",
        "Helper2Shuffle",
        "Helper4Bridge",
        "Helper4Leaf",
        "SharedLeaf",
        "Helper5Bridge",
        "Helper5Leaf",
        "WeightedB",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "MainBehavior",
        "MainBehavior",
        "MainBehavior",
        "LocalBranch",
        "LocalA",
        "LocalB",
        "ShuffleTail",
        "ImportedBranch",
        "WeightedA",
        "Helper2Shuffle",
        "Helper4Bridge",
        "Helper5Bridge",
        "WeightedB",
    ]
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "parallel",
        "parallel",
        "choose",
        "parallel",
        "parallel",
        "shuffle",
        "choose",
        "parallel",
        "shuffle",
        "parallel",
        "parallel",
        "choose",
    ]
    assert [statement.node_id for statement in graph.statements] == [
        "MainBehavior:1",
        "MainBehavior:2",
        "MainBehavior:3",
        "LocalBranch:1",
        "LocalA:1",
        "LocalB:1",
        "ShuffleTail:1",
        "ImportedBranch:1",
        "WeightedA:1",
        "Helper2Shuffle:1",
        "Helper4Bridge:1",
        "Helper5Bridge:1",
        "WeightedB:1",
    ]


def test_main_scenic_contains_expected_random_and_weighted_invocations():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)
    by_container = {statement.container_name: statement for statement in graph.statements}

    local_branch = by_container["LocalBranch"]
    imported = by_container["ImportedBranch"]
    shuffle_tail = by_container["ShuffleTail"]
    weighted_b = by_container["WeightedB"]
    helper2_shuffle = by_container["Helper2Shuffle"]

    assert [inv.target for inv in local_branch.invocations] == ["LocalA", "LocalB"]
    assert [inv.weight for inv in local_branch.invocations] == [None, None]

    assert [inv.target for inv in imported.invocations] == ["WeightedA", "WeightedB"]
    assert [inv.weight for inv in imported.invocations] == [2.0, 1.0]
    assert all(inv.is_weighted for inv in imported.invocations)

    assert [inv.target for inv in shuffle_tail.invocations] == ["TailA", "TailB"]
    assert [inv.target for inv in weighted_b.invocations] == [
        "Helper4Bridge",
        "Helper5Bridge",
    ]
    assert [inv.weight for inv in weighted_b.invocations] == [3.0, 1.0]
    assert [inv.target for inv in helper2_shuffle.invocations] == [
        "Helper4Leaf",
        "Helper5Leaf",
    ]


def test_main_scenic_graph_has_expected_next_edges_only_for_main_behavior():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)

    next_edges = [edge for edge in graph.edges if edge.kind == "next"]

    assert [(edge.source, edge.target) for edge in next_edges] == [
        ("MainBehavior:1", "MainBehavior:2"),
        ("MainBehavior:2", "MainBehavior:3"),
    ]
    assert [edge.attributes["within"] for edge in next_edges] == [
        "MainBehavior",
        "MainBehavior",
    ]


def test_main_scenic_execution_structure_has_expected_start_points_and_invocations():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)
    execution = build_execution_structure(graph)

    assert execution.container_ids[0] == "initial:<initial>"
    assert execution.containers["behavior:MainBehavior"]["start_ids"] == [
        "MainBehavior:1"
    ]
    assert execution.compositions["MainBehavior:1"]["next_ids"] == ["MainBehavior:2"]
    assert execution.compositions["MainBehavior:2"]["next_ids"] == ["MainBehavior:3"]
    assert execution.compositions["ImportedBranch:1"]["invocation_ids"] == [
        "ImportedBranch:1:invocation:0",
        "ImportedBranch:1:invocation:1",
    ]
    assert execution.invocations["ImportedBranch:1:invocation:0"].attributes["weight"] == 2.0
    assert execution.invocations["ImportedBranch:1:invocation:1"].attributes["weight"] == 1.0
    assert execution.compositions["WeightedB:1"]["invocation_ids"] == [
        "WeightedB:1:invocation:0",
        "WeightedB:1:invocation:1",
    ]
    assert execution.invocations["WeightedB:1:invocation:0"].attributes["weight"] == 3.0
    assert execution.invocations["WeightedB:1:invocation:1"].attributes["weight"] == 1.0


def test_main_scenic_sxo_structure_has_recursive_and_weighted_edges():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)
    sxo = build_sxo_structure(graph)

    node_ids = {node.id for node in sxo.nodes}
    edge_triples = {(edge.source, edge.target, edge.kind) for edge in sxo.edges}

    assert "S:behavior:ImportedBranch" in node_ids
    assert "X:ImportedBranch:1" in node_ids
    assert "O:ImportedBranch:1:invocation:0" in node_ids

    assert (
        "O:MainBehavior:2:invocation:0",
        "S:behavior:ImportedBranch",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:ImportedBranch:1:invocation:0",
        "S:behavior:WeightedA",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:ImportedBranch:1:invocation:1",
        "S:behavior:WeightedB",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:WeightedB:1:invocation:0",
        "S:behavior:Helper4Bridge",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:WeightedB:1:invocation:1",
        "S:behavior:Helper5Bridge",
        "O_targets_S",
    ) in edge_triples
    weighted_edges = {
        (edge.source, edge.target): edge.attributes["weight"]
        for edge in sxo.edges
        if edge.kind == "X_to_O" and edge.attributes.get("weight") is not None
    }
    assert weighted_edges == {
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:0"): 2.0,
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:1"): 1.0,
        ("X:WeightedB:1", "O:WeightedB:1:invocation:0"): 3.0,
        ("X:WeightedB:1", "O:WeightedB:1:invocation:1"): 1.0,
    }


def test_main_scenic_compact_graph_has_probabilities_weights_and_recursive_targets():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)
    compact = build_compact_graph_dict(graph)

    assert compact["nodes"]["X:LocalBranch:1"] == {
        "type": "X",
        "op": "choose",
        "container": "LocalBranch",
    }
    assert compact["nodes"]["X:ImportedBranch:1"] == {
        "type": "X",
        "op": "choose",
        "container": "ImportedBranch",
    }
    assert compact["nodes"]["X:ShuffleTail:1"] == {
        "type": "X",
        "op": "shuffle",
        "container": "ShuffleTail",
    }
    assert compact["nodes"]["X:WeightedB:1"] == {
        "type": "X",
        "op": "choose",
        "container": "WeightedB",
    }

    compact_edges = {
        (edge["source"], edge["target"], edge["type"]): edge
        for edge in compact["edges"]
    }
    assert compact_edges[
        ("X:LocalBranch:1", "O:LocalBranch:1:invocation:0", "X_to_O")
    ]["probability"] == 0.5
    assert compact_edges[
        ("X:LocalBranch:1", "O:LocalBranch:1:invocation:1", "X_to_O")
    ]["probability"] == 0.5
    assert compact_edges[
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:0", "X_to_O")
    ]["weight"] == 2.0
    assert compact_edges[
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:0", "X_to_O")
    ]["probability"] == pytest.approx(2 / 3)
    assert compact_edges[
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:1", "X_to_O")
    ]["weight"] == 1.0
    assert compact_edges[
        ("X:ImportedBranch:1", "O:ImportedBranch:1:invocation:1", "X_to_O")
    ]["probability"] == pytest.approx(1 / 3)
    assert compact_edges[
        ("X:WeightedB:1", "O:WeightedB:1:invocation:0", "X_to_O")
    ]["weight"] == 3.0
    assert compact_edges[
        ("X:WeightedB:1", "O:WeightedB:1:invocation:0", "X_to_O")
    ]["probability"] == pytest.approx(0.75)
    assert compact_edges[
        ("X:WeightedB:1", "O:WeightedB:1:invocation:1", "X_to_O")
    ]["weight"] == 1.0
    assert compact_edges[
        ("X:WeightedB:1", "O:WeightedB:1:invocation:1", "X_to_O")
    ]["probability"] == pytest.approx(0.25)
    assert (
        "O:MainBehavior:2:invocation:0",
        "S:behavior:ImportedBranch",
        "O_targets_S",
    ) in compact_edges


def test_main_scenic_sample_trace_is_recursive_and_respects_random_choices():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)

    for _ in range(20):
        trace = sample_from_graph(graph)
        assert trace[0] == "LocalBranch"
        assert trace[1] in {"LocalA", "LocalB"}
        assert trace[2] == "LocalLeaf"
        assert trace[3] == "ImportedBranch"
        assert trace[4] in {"WeightedA", "WeightedB"}
        if trace[4] == "WeightedA":
            assert trace[5:7] == ["Helper4Bridge", "SharedLeaf"]
            shuffle_index = 7
        else:
            assert trace[5] in {"Helper4Bridge", "Helper5Bridge"}
            if trace[5] == "Helper4Bridge":
                assert trace[6] == "SharedLeaf"
            else:
                assert trace[6] == "Helper2Leaf"
            shuffle_index = 7
        assert trace[shuffle_index] == "ShuffleTail"
        assert trace[shuffle_index + 1 : shuffle_index + 3] in (
            ["TailA", "TailB"],
            ["TailB", "TailA"],
        )


def test_main_scenic_sample_trace_can_reach_all_branches():
    graph = analyze_scenic_composition(SCENIC_TEST_MAIN)

    local_choices = set()
    imported_choices = set()
    weighted_b_choices = set()
    shuffle_orders = set()

    for _ in range(200):
        trace = sample_from_graph(graph)
        local_choices.add(trace[1])
        imported_choices.add(trace[4])
        if trace[4] == "WeightedB":
            weighted_b_choices.add(trace[5])
        shuffle_start = trace.index("ShuffleTail") + 1
        shuffle_orders.add(tuple(trace[shuffle_start : shuffle_start + 2]))

    assert local_choices == {"LocalA", "LocalB"}
    assert imported_choices == {"WeightedA", "WeightedB"}
    assert weighted_b_choices == {"Helper4Bridge", "Helper5Bridge"}
    assert shuffle_orders == {("TailA", "TailB"), ("TailB", "TailA")}


def test_main_scenic_analysis_output_includes_all_layers_and_recursive_data():
    output = build_analysis_output(SCENIC_TEST_MAIN)

    assert set(output.keys()) == {
        "graph",
        "execution_structure",
        "sxo_structure",
        "compact_graph",
        "partner_format",
        "sample_trace",
    }
    assert output["graph"]["container_names"][1] == "MainBehavior"
    assert "S:behavior:ImportedBranch" in output["compact_graph"]["nodes"]
    assert any(
        edge["type"] == "O_targets_S"
        and edge["target"] == "S:behavior:ImportedBranch"
        for edge in output["compact_graph"]["edges"]
    )
    assert "S:behavior:Helper5Bridge" in output["compact_graph"]["nodes"]
    assert output["sample_trace"][0] == "LocalBranch"


def test_case_straight_builds_linear_recursive_graph():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "LocalStart",
        "LocalLeft",
        "LocalRight",
        "TailShuffle",
        "TailA",
        "TailB",
        "ImportedChain",
        "Helper2Branch",
        "Helper3A",
        "Helper3B",
        "StraightLeaf",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "MainBehavior",
        "MainBehavior",
        "MainBehavior",
        "LocalStart",
        "TailShuffle",
        "ImportedChain",
        "Helper2Branch",
        "Helper3A",
        "Helper3B",
    ]
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "parallel",
        "parallel",
        "choose",
        "shuffle",
        "parallel",
        "choose",
        "parallel",
        "parallel",
    ]
    assert [statement.node_id for statement in graph.statements] == [
        "MainBehavior:1",
        "MainBehavior:2",
        "MainBehavior:3",
        "LocalStart:1",
        "TailShuffle:1",
        "ImportedChain:1",
        "Helper2Branch:1",
        "Helper3A:1",
        "Helper3B:1",
    ]


def test_case_straight_has_expected_linear_recursion_and_weights():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)
    by_node_id = {statement.node_id: statement for statement in graph.statements}

    assert [inv.target for inv in by_node_id["MainBehavior:1"].invocations] == ["LocalStart"]
    assert [inv.target for inv in by_node_id["MainBehavior:2"].invocations] == [
        "ImportedChain"
    ]
    assert [inv.target for inv in by_node_id["MainBehavior:3"].invocations] == [
        "TailShuffle"
    ]
    assert [inv.target for inv in by_node_id["LocalStart:1"].invocations] == [
        "LocalLeft",
        "LocalRight",
    ]
    assert [inv.weight for inv in by_node_id["LocalStart:1"].invocations] == [None, None]
    assert [inv.target for inv in by_node_id["ImportedChain:1"].invocations] == [
        "Helper2Branch"
    ]
    assert [inv.target for inv in by_node_id["Helper2Branch:1"].invocations] == [
        "Helper3A",
        "Helper3B",
    ]
    assert [inv.weight for inv in by_node_id["Helper2Branch:1"].invocations] == [2.0, 1.0]


def test_case_straight_execution_and_sxo_structures_show_chain():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)
    execution = build_execution_structure(graph)
    sxo = build_sxo_structure(graph)

    assert execution.containers["behavior:MainBehavior"]["start_ids"] == ["MainBehavior:1"]
    assert execution.compositions["MainBehavior:1"]["next_ids"] == ["MainBehavior:2"]
    assert execution.compositions["MainBehavior:2"]["next_ids"] == ["MainBehavior:3"]
    assert execution.compositions["Helper2Branch:1"]["invocation_ids"] == [
        "Helper2Branch:1:invocation:0",
        "Helper2Branch:1:invocation:1",
    ]

    edge_triples = {(edge.source, edge.target, edge.kind) for edge in sxo.edges}
    assert (
        "O:MainBehavior:2:invocation:0",
        "S:behavior:ImportedChain",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:ImportedChain:1:invocation:0",
        "S:behavior:Helper2Branch",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:Helper2Branch:1:invocation:0",
        "S:behavior:Helper3A",
        "O_targets_S",
    ) in edge_triples
    assert (
        "O:Helper2Branch:1:invocation:1",
        "S:behavior:Helper3B",
        "O_targets_S",
    ) in edge_triples


def test_case_straight_compact_graph_has_probabilities_and_recursive_targets():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)
    compact = build_compact_graph_dict(graph)

    assert compact["nodes"]["X:LocalStart:1"] == {
        "type": "X",
        "op": "choose",
        "container": "LocalStart",
    }
    assert compact["nodes"]["X:Helper2Branch:1"] == {
        "type": "X",
        "op": "choose",
        "container": "Helper2Branch",
    }
    compact_edges = {
        (edge["source"], edge["target"], edge["type"]): edge
        for edge in compact["edges"]
    }
    assert compact_edges[
        ("X:LocalStart:1", "O:LocalStart:1:invocation:0", "X_to_O")
    ]["probability"] == 0.5
    assert compact_edges[
        ("X:LocalStart:1", "O:LocalStart:1:invocation:1", "X_to_O")
    ]["probability"] == 0.5
    assert compact_edges[
        ("X:Helper2Branch:1", "O:Helper2Branch:1:invocation:0", "X_to_O")
    ]["weight"] == 2.0
    assert compact_edges[
        ("X:Helper2Branch:1", "O:Helper2Branch:1:invocation:0", "X_to_O")
    ]["probability"] == pytest.approx(2 / 3)
    assert compact_edges[
        ("X:Helper2Branch:1", "O:Helper2Branch:1:invocation:1", "X_to_O")
    ]["weight"] == 1.0
    assert compact_edges[
        ("X:Helper2Branch:1", "O:Helper2Branch:1:invocation:1", "X_to_O")
    ]["probability"] == pytest.approx(1 / 3)
    assert (
        "O:ImportedChain:1:invocation:0",
        "S:behavior:Helper2Branch",
        "O_targets_S",
    ) in compact_edges


def test_case_straight_sample_trace_follows_chain_and_random_choices():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)

    local_choices = set()
    imported_choices = set()
    shuffle_orders = set()

    for _ in range(100):
        trace = sample_from_graph(graph)
        assert trace[0] == "LocalStart"
        assert trace[1] in {"LocalLeft", "LocalRight"}
        local_choices.add(trace[1])
        assert trace[2] == "ImportedChain"
        assert trace[3] == "Helper2Branch"
        assert trace[4] in {"Helper3A", "Helper3B"}
        imported_choices.add(trace[4])
        assert trace[5] == "StraightLeaf"
        assert trace[6] == "TailShuffle"
        shuffle_orders.add(tuple(trace[7:9]))

    assert local_choices == {"LocalLeft", "LocalRight"}
    assert imported_choices == {"Helper3A", "Helper3B"}
    assert shuffle_orders == {("TailA", "TailB"), ("TailB", "TailA")}


def test_case_straight_analysis_output_includes_linear_chain():
    output = build_analysis_output(SCENIC_TEST_STRAIGHT)

    assert set(output.keys()) == {
        "graph",
        "execution_structure",
        "sxo_structure",
        "compact_graph",
        "partner_format",
        "sample_trace",
    }
    assert output["graph"]["container_names"][1] == "MainBehavior"
    assert "S:behavior:ImportedChain" in output["compact_graph"]["nodes"]
    assert "S:behavior:Helper2Branch" in output["compact_graph"]["nodes"]
    assert any(
        edge["type"] == "O_targets_S"
        and edge["target"] == "S:behavior:Helper2Branch"
        for edge in output["compact_graph"]["edges"]
    )
    assert output["sample_trace"][0] == "LocalStart"


def test_case_scenario_builds_scenario_and_behavior_graph():
    graph = analyze_scenic_composition(SCENIC_TEST_SCENARIO)

    assert graph.container_names == (
        "<initial>",
        "Main",
        "LocalScenario",
        "AlternateScenario",
        "LocalBehavior",
        "ImportedBehavior",
        "ImportedScenario",
        "ImportedLeaf",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "Main",
        "Main",
        "LocalScenario",
        "AlternateScenario",
        "ImportedBehavior",
        "ImportedScenario",
    ]
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "choose",
        "parallel",
        "parallel",
        "parallel",
        "parallel",
    ]


def test_case_scenario_compact_graph_links_scenarios_and_behaviors():
    graph = analyze_scenic_composition(SCENIC_TEST_SCENARIO)
    compact = build_compact_graph_dict(graph)

    assert compact["nodes"]["S:scenario:Main"]["type"] == "S"
    assert compact["nodes"]["S:scenario:ImportedScenario"]["type"] == "S"
    assert compact["nodes"]["X:Main:2"] == {
        "type": "X",
        "op": "choose",
        "container": "Main",
    }
    compact_edges = {
        (edge["source"], edge["target"], edge["type"]): edge
        for edge in compact["edges"]
    }
    assert (
        "O:Main:1:invocation:0",
        "S:scenario:ImportedScenario",
        "O_targets_S",
    ) in compact_edges
    assert (
        "O:ImportedScenario:1:invocation:0",
        "S:behavior:ImportedBehavior",
        "O_targets_S",
    ) in compact_edges
    assert compact_edges[("X:Main:2", "O:Main:2:invocation:0", "X_to_O")][
        "probability"
    ] == 0.5
    assert compact_edges[("X:Main:2", "O:Main:2:invocation:1", "X_to_O")][
        "probability"
    ] == 0.5


def test_case_scenario_sample_trace_reaches_imported_and_local_scenarios():
    graph = analyze_scenic_composition(SCENIC_TEST_SCENARIO)

    local_choices = set()
    for _ in range(40):
        trace = sample_from_graph(graph)
        assert trace[:3] == ["ImportedScenario", "ImportedBehavior", "ImportedLeaf"]
        assert trace[3] in {"LocalScenario", "AlternateScenario"}
        assert trace[4] == "LocalBehavior"
        local_choices.add(trace[3])

    assert local_choices == {"LocalScenario", "AlternateScenario"}


def test_case_interrupt_temporal_captures_try_until_and_for():
    graph = analyze_scenic_composition(SCENIC_TEST_INTERRUPT)
    execution = build_execution_structure(graph)
    compact = build_compact_graph_dict(graph)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "BaseBehavior",
        "InterruptBehavior",
        "TimedBehavior",
    )
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "until",
        "for",
    ]
    assert [statement.nesting for statement in graph.statements] == [
        ("try",),
        ("try", "interrupt when simulation().currentTime > 1"),
        ("try", "interrupt when simulation().currentTime > 1"),
    ]
    assert execution.compositions["MainBehavior:1"]["next_ids"] == ["MainBehavior:2"]
    assert execution.compositions["MainBehavior:2"]["next_ids"] == ["MainBehavior:3"]
    assert compact["nodes"]["X:MainBehavior:2"] == {
        "type": "X",
        "op": "until",
        "container": "MainBehavior",
    }
    assert compact["nodes"]["X:MainBehavior:3"] == {
        "type": "X",
        "op": "for",
        "container": "MainBehavior",
    }
    assert sample_from_graph(graph) == [
        "BaseBehavior",
        "InterruptBehavior",
        "TimedBehavior",
    ]


def test_case_monitor_require_parses_behavior_graph_without_breaking():
    graph = analyze_scenic_composition(SCENIC_TEST_MONITOR)
    compact = build_compact_graph_dict(graph)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "BranchBehavior",
        "LeafA",
        "LeafB",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "MainBehavior",
        "BranchBehavior",
    ]
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "choose",
    ]
    assert compact["nodes"]["X:BranchBehavior:1"] == {
        "type": "X",
        "op": "choose",
        "container": "BranchBehavior",
    }
    trace = sample_from_graph(graph)
    assert trace[0] == "BranchBehavior"
    assert trace[1] in {"LeafA", "LeafB"}


def test_case_weighted_shuffle_preserves_weights_in_graph_and_compact_export():
    graph = analyze_scenic_composition(SCENIC_TEST_WEIGHTED_SHUFFLE)
    compact = build_compact_graph_dict(graph)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "WeightedShuffle",
        "HeavyLeaf",
        "LightLeaf",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "MainBehavior",
        "WeightedShuffle",
    ]
    assert [statement.operator for statement in graph.statements] == [
        "parallel",
        "shuffle",
    ]
    weighted_shuffle = graph.statements[1]
    assert [inv.target for inv in weighted_shuffle.invocations] == [
        "HeavyLeaf",
        "LightLeaf",
    ]
    assert [inv.weight for inv in weighted_shuffle.invocations] == [3.0, 1.0]

    compact_edges = {
        (edge["source"], edge["target"], edge["type"]): edge
        for edge in compact["edges"]
    }
    assert compact["nodes"]["X:WeightedShuffle:1"] == {
        "type": "X",
        "op": "shuffle",
        "container": "WeightedShuffle",
    }
    assert compact_edges[
        ("X:WeightedShuffle:1", "O:WeightedShuffle:1:invocation:0", "X_to_O")
    ]["weight"] == 3.0
    assert compact_edges[
        ("X:WeightedShuffle:1", "O:WeightedShuffle:1:invocation:1", "X_to_O")
    ]["weight"] == 1.0


def test_case_weighted_shuffle_sampling_biases_heavier_item_earlier():
    graph = analyze_scenic_composition(SCENIC_TEST_WEIGHTED_SHUFFLE)

    heavy_first = 0
    light_first = 0
    for _ in range(400):
        trace = sample_from_graph(graph)
        assert trace[0] == "WeightedShuffle"
        assert set(trace[1:3]) == {"HeavyLeaf", "LightLeaf"}
        if trace[1] == "HeavyLeaf":
            heavy_first += 1
        else:
            light_first += 1

    assert heavy_first > light_first


def test_build_partner_format_exports_container_steps_for_straight_case():
    graph = analyze_scenic_composition(SCENIC_TEST_STRAIGHT)
    partner = build_partner_format(graph)

    assert partner["entrypoints"] == ["MainBehavior"]
    assert partner["containers"]["MainBehavior"] == {
        "kind": "behavior",
        "steps": ["LocalStart", "ImportedChain", "TailShuffle"],
    }
    assert partner["containers"]["LocalStart"] == {
        "kind": "behavior",
        "steps": [{"LocalLeft": 0.5, "LocalRight": 0.5}],
    }
    assert partner["containers"]["ImportedChain"] == {
        "kind": "behavior",
        "steps": ["Helper2Branch"],
    }
    assert partner["containers"]["Helper2Branch"] == {
        "kind": "behavior",
        "steps": [{"Helper3A": pytest.approx(2 / 3), "Helper3B": pytest.approx(1 / 3)}],
    }


def test_build_partner_format_exports_shuffle_in_structured_form():
    graph = analyze_scenic_composition(SCENIC_TEST_WEIGHTED_SHUFFLE)
    partner = build_partner_format(graph)

    assert partner["entrypoints"] == ["MainBehavior"]
    assert partner["containers"]["MainBehavior"] == {
        "kind": "behavior",
        "steps": ["WeightedShuffle"],
    }
    assert partner["containers"]["WeightedShuffle"] == {
        "kind": "behavior",
        "steps": [
            {
                "shuffle": {
                    "HeavyLeaf": pytest.approx(0.75),
                    "LightLeaf": pytest.approx(0.25),
                }
            }
        ],
    }


@pytest.mark.parametrize("path_str", REALISTIC_CASES)
def test_realistic_cases_analyze_build_and_sample_end_to_end(path_str):
    graph = analyze_scenic_composition(path_str)
    execution = build_execution_structure(graph)
    sxo = build_sxo_structure(graph)
    compact = build_compact_graph_dict(graph)
    partner = build_partner_format(graph)
    output = build_analysis_output(path_str)
    sample = sample_from_graph(graph)

    assert graph.source_kind == "path"
    assert graph.source_path and graph.source_path.endswith("main.scenic")
    assert len(graph.container_names) >= 10
    assert "Main" in graph.container_names
    assert len(graph.statements) >= 10
    assert any(statement.operator == "choose" for statement in graph.statements)
    assert any(statement.operator == "shuffle" for statement in graph.statements)
    assert any(statement.operator == "until" for statement in graph.statements)
    assert any(statement.operator == "for" for statement in graph.statements)

    edge_kinds = [edge.kind for edge in graph.edges]
    assert "contains" in edge_kinds
    assert "invokes" in edge_kinds
    assert "next" in edge_kinds

    assert "scenario:Main" in execution.containers
    assert execution.containers["scenario:Main"]["start_ids"]

    sxo_edge_kinds = [edge.kind for edge in sxo.edges]
    assert "S_to_X" in sxo_edge_kinds
    assert "X_to_O" in sxo_edge_kinds
    assert "O_targets_S" in sxo_edge_kinds

    assert "S:scenario:Main" in compact["nodes"]
    assert any(edge["type"] == "O_targets_S" for edge in compact["edges"])
    assert any(edge["type"] == "X_to_O" and "weight" in edge for edge in compact["edges"])

    assert "Main" in partner["containers"]
    assert partner["containers"]["Main"]["kind"] == "scenario"
    assert partner["containers"]["Main"]["steps"]

    assert sample
    assert isinstance(sample[0], str)

    assert set(output.keys()) == {
        "graph",
        "execution_structure",
        "sxo_structure",
        "compact_graph",
        "partner_format",
        "sample_trace",
    }
    assert output["graph"]["container_names"][1] == "Main"
    assert output["partner_format"]["containers"]["Main"]["kind"] == "scenario"
    assert output["sample_trace"]


def test_analyze_scenic_composition_includes_local_scenic_imports(tmp_path):
    helper = tmp_path / "helper.scenic"
    helper.write_text(
        "behavior ImportedBehavior():\n"
        "    do LeafBehavior()\n",
        encoding="utf-8",
    )
    main = tmp_path / "main.scenic"
    main.write_text(
        "from helper import *\n\n"
        "behavior MainBehavior():\n"
        "    do ImportedBehavior()\n",
        encoding="utf-8",
    )

    graph = analyze_scenic_composition(main)
    output = build_analysis_output(main)

    assert graph.container_names == (
        "<initial>",
        "MainBehavior",
        "ImportedBehavior",
    )
    assert [statement.container_name for statement in graph.statements] == [
        "MainBehavior",
        "ImportedBehavior",
    ]
    assert sample_from_graph(graph) == ["ImportedBehavior", "LeafBehavior"]
    assert "S:behavior:ImportedBehavior" in output["compact_graph"]["nodes"]
