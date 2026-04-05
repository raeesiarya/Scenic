from pathlib import Path
import sys

import pytest

from tools.scenic_composition_analysis_helpers import (
    Container,
    CompositionGraph,
    CompositionStatement,
    ExecutionStructure,
    GraphEdge,
    GraphNode,
    InvocationSpec,
    SXONode,
    SXOStructure,
    SxOEdge,
    choose_invocation,
    extract_from_parser,
    invocation_result,
    load_source,
    operator_semantics,
    ordered_compositions,
    parse_weight,
    sample_composition,
    sort_node_ids,
    target_name,
)

SCENIC_TEST_MAIN = Path("examples/scenic_tests/case_interconnected/main.scenic")
SCENIC_TEST_HELPER1 = Path("examples/scenic_tests/case_interconnected/helper1.scenic")
SCENIC_TEST_HELPER2 = Path("examples/scenic_tests/case_interconnected/helper2.scenic")
SCENIC_TEST_HELPER3 = Path("examples/scenic_tests/case_interconnected/helper3.scenic")
SCENIC_TEST_HELPER4 = Path("examples/scenic_tests/case_interconnected/helper4.scenic")
SCENIC_TEST_HELPER5 = Path("examples/scenic_tests/case_interconnected/helper5.scenic")
SCENIC_TEST_STRAIGHT_MAIN = Path("examples/scenic_tests/case_straight/main.scenic")
SCENIC_TEST_STRAIGHT_HELPER1 = Path("examples/scenic_tests/case_straight/helper1.scenic")
SCENIC_TEST_STRAIGHT_HELPER2 = Path("examples/scenic_tests/case_straight/helper2.scenic")
SCENIC_TEST_STRAIGHT_HELPER3 = Path("examples/scenic_tests/case_straight/helper3.scenic")
SCENIC_TEST_SCENARIO_MAIN = Path("examples/scenic_tests/case_scenario/main.scenic")
SCENIC_TEST_SCENARIO_HELPER1 = Path("examples/scenic_tests/case_scenario/helper1.scenic")
SCENIC_TEST_INTERRUPT_MAIN = Path(
    "examples/scenic_tests/case_interrupt_temporal/main.scenic"
)
SCENIC_TEST_MONITOR_MAIN = Path(
    "examples/scenic_tests/case_monitor_require/main.scenic"
)


EXAMPLE_CASES = [
    (
        "examples/driving/OAS_Scenarios/oas_scenario_03.scenic",
        ["<initial>", "CollisionAvoidance", "FollowLeadCarBehavior"],
        2,
    ),
    (
        "examples/driving/OAS_Scenarios/oas_scenario_04.scenic",
        ["<initial>", "LeadCarBehavior", "CollisionAvoidance", "FollowLeadCarBehavior"],
        3,
    ),
    (
        "examples/driving/OAS_Scenarios/oas_scenario_28.scenic",
        ["<initial>", "EgoBehavior", "OtherCarBehavior"],
        2,
    ),
    (
        "examples/driving/OAS_Scenarios/oas_scenario_29.scenic",
        ["<initial>", "EgoBehavior"],
        1,
    ),
    (
        "examples/driving/OAS_Scenarios/oas_scenario_30.scenic",
        ["<initial>", "SafeBehavior", "EgoBehavior"],
        2,
    ),
    (
        "examples/driving/OAS_Scenarios/oas_scenario_32.scenic",
        ["<initial>", "FollowTrafficBehavior", "SafeBehavior"],
        2,
    ),
    (
        "examples/driving/Carla_Challenge/carlaChallenge2.scenic",
        ["<initial>", "EgoBehavior", "LeadingCarBehavior"],
        2,
    ),
    (
        "examples/driving/Carla_Challenge/carlaChallenge3.scenic",
        ["<initial>", "EgoBehavior"],
        1,
    ),
]


def test_load_source_from_string():
    text, source_path, source_kind = load_source("behavior Foo():\n    do Bar()")

    assert text == "behavior Foo():\n    do Bar()"
    assert source_path is None
    assert source_kind == "string"


def test_load_source_from_path():
    path = Path("examples/driving/OAS_Scenarios/oas_scenario_03.scenic")

    text, source_path, source_kind = load_source(path)

    assert "behavior FollowLeadCarBehavior" in text
    assert source_path == path.resolve()
    assert source_kind == "path"


def test_load_source_from_main_scenic_test_path():
    text, source_path, source_kind = load_source(SCENIC_TEST_MAIN)

    assert "behavior MainBehavior" in text
    assert "do ImportedBranch()" in text
    assert source_path == SCENIC_TEST_MAIN.resolve()
    assert source_kind == "path"


@pytest.mark.parametrize(
    "path_obj, expected_line",
    [
        (SCENIC_TEST_HELPER1, "behavior ImportedBranch():"),
        (SCENIC_TEST_HELPER2, "behavior WeightedA():"),
        (SCENIC_TEST_HELPER3, "behavior WeightedB():"),
        (SCENIC_TEST_HELPER4, "behavior Helper4Bridge():"),
        (SCENIC_TEST_HELPER5, "behavior Helper5Bridge():"),
    ],
)
def test_load_source_from_each_interconnected_helper(path_obj, expected_line):
    text, source_path, source_kind = load_source(path_obj)

    assert expected_line in text
    assert source_path == path_obj.resolve()
    assert source_kind == "path"


@pytest.mark.parametrize(
    "path_str, expected_containers, expected_statement_count", EXAMPLE_CASES
)
def test_extract_from_parser_matches_real_examples(
    path_str, expected_containers, expected_statement_count
):
    text = Path(path_str).read_text()

    containers, statements = extract_from_parser(text)

    assert [container.name for container in containers] == expected_containers
    assert all(isinstance(container, Container) for container in containers)
    assert len(statements) == expected_statement_count
    assert all(isinstance(statement, CompositionStatement) for statement in statements)
    assert all(statement.operator == "parallel" for statement in statements)


def test_extract_from_parser_captures_try_interrupt_structure():
    text = Path("examples/driving/OAS_Scenarios/oas_scenario_04.scenic").read_text()

    containers, statements = extract_from_parser(text)

    assert [container.name for container in containers] == [
        "<initial>",
        "LeadCarBehavior",
        "CollisionAvoidance",
        "FollowLeadCarBehavior",
    ]
    assert [statement.container_name for statement in statements] == [
        "LeadCarBehavior",
        "FollowLeadCarBehavior",
        "FollowLeadCarBehavior",
    ]
    assert statements[0].invocations[0].target == "FollowLaneBehavior"
    assert statements[0].nesting == ("try",)
    assert statements[1].invocations[0].text == "FollowLaneBehavior()"
    assert statements[1].invocations[0].target == "FollowLaneBehavior"
    assert statements[1].nesting == ("try",)
    assert statements[2].nesting == (
        "try",
        "interrupt when withinDistanceToAnyObjs(self, SAFETY_DISTANCE)",
    )
    assert statements[2].invocations[0].target == "CollisionAvoidance"


def test_extract_from_parser_captures_random_and_recursive_local_structure_in_main_scenic():
    text = SCENIC_TEST_MAIN.read_text()

    containers, statements = extract_from_parser(text)

    assert [container.name for container in containers] == [
        "<initial>",
        "MainBehavior",
        "LocalBranch",
        "LocalA",
        "LocalB",
        "LocalLeaf",
        "ShuffleTail",
        "TailA",
        "TailB",
    ]
    assert [statement.container_name for statement in statements] == [
        "MainBehavior",
        "MainBehavior",
        "MainBehavior",
        "LocalBranch",
        "LocalA",
        "LocalB",
        "ShuffleTail",
    ]
    assert [statement.operator for statement in statements] == [
        "parallel",
        "parallel",
        "parallel",
        "choose",
        "parallel",
        "parallel",
        "shuffle",
    ]
    assert [statement.node_id for statement in statements] == [
        "MainBehavior:1",
        "MainBehavior:2",
        "MainBehavior:3",
        "LocalBranch:1",
        "LocalA:1",
        "LocalB:1",
        "ShuffleTail:1",
    ]


def test_extract_from_parser_captures_weighted_choose_in_helper_scenic():
    text = SCENIC_TEST_HELPER1.read_text()

    containers, statements = extract_from_parser(text)

    assert [container.name for container in containers] == [
        "<initial>",
        "ImportedBranch",
    ]
    assert [statement.container_name for statement in statements] == [
        "ImportedBranch",
    ]
    assert [statement.operator for statement in statements] == [
        "choose",
    ]
    imported = statements[0]
    assert [inv.text for inv in imported.invocations] == ["WeightedA()", "WeightedB()"]
    assert [inv.target for inv in imported.invocations] == ["WeightedA", "WeightedB"]
    assert [inv.weight for inv in imported.invocations] == [2.0, 1.0]
    assert all(inv.is_weighted for inv in imported.invocations)


def test_extract_from_parser_captures_helper2_helper3_helper4_helper5_structures():
    helper2_containers, helper2_statements = extract_from_parser(
        SCENIC_TEST_HELPER2.read_text()
    )
    helper3_containers, helper3_statements = extract_from_parser(
        SCENIC_TEST_HELPER3.read_text()
    )
    helper4_containers, helper4_statements = extract_from_parser(
        SCENIC_TEST_HELPER4.read_text()
    )
    helper5_containers, helper5_statements = extract_from_parser(
        SCENIC_TEST_HELPER5.read_text()
    )

    assert [container.name for container in helper2_containers] == [
        "<initial>",
        "WeightedA",
        "Helper2Leaf",
        "Helper2Shuffle",
    ]
    assert [statement.container_name for statement in helper2_statements] == [
        "WeightedA",
        "Helper2Shuffle",
    ]
    assert [statement.operator for statement in helper2_statements] == [
        "parallel",
        "shuffle",
    ]
    assert [inv.target for inv in helper2_statements[1].invocations] == [
        "Helper4Leaf",
        "Helper5Leaf",
    ]

    assert [container.name for container in helper3_containers] == [
        "<initial>",
        "WeightedB",
    ]
    assert [statement.container_name for statement in helper3_statements] == [
        "WeightedB"
    ]
    assert helper3_statements[0].operator == "choose"
    assert [inv.target for inv in helper3_statements[0].invocations] == [
        "Helper4Bridge",
        "Helper5Bridge",
    ]
    assert [inv.weight for inv in helper3_statements[0].invocations] == [3.0, 1.0]

    assert [container.name for container in helper4_containers] == [
        "<initial>",
        "Helper4Bridge",
        "Helper4Leaf",
        "SharedLeaf",
    ]
    assert [statement.container_name for statement in helper4_statements] == [
        "Helper4Bridge"
    ]
    assert helper4_statements[0].invocations[0].target == "SharedLeaf"

    assert [container.name for container in helper5_containers] == [
        "<initial>",
        "Helper5Bridge",
        "Helper5Leaf",
    ]
    assert [statement.container_name for statement in helper5_statements] == [
        "Helper5Bridge"
    ]
    assert helper5_statements[0].invocations[0].target == "Helper2Leaf"


def test_extract_from_parser_captures_case_straight_local_structure():
    containers, statements = extract_from_parser(SCENIC_TEST_STRAIGHT_MAIN.read_text())

    assert [container.name for container in containers] == [
        "<initial>",
        "MainBehavior",
        "LocalStart",
        "LocalLeft",
        "LocalRight",
        "TailShuffle",
        "TailA",
        "TailB",
    ]
    assert [statement.container_name for statement in statements] == [
        "MainBehavior",
        "MainBehavior",
        "MainBehavior",
        "LocalStart",
        "TailShuffle",
    ]
    assert [statement.operator for statement in statements] == [
        "parallel",
        "parallel",
        "parallel",
        "choose",
        "shuffle",
    ]


def test_extract_from_parser_captures_case_straight_helper_chain():
    helper1_containers, helper1_statements = extract_from_parser(
        SCENIC_TEST_STRAIGHT_HELPER1.read_text()
    )
    helper2_containers, helper2_statements = extract_from_parser(
        SCENIC_TEST_STRAIGHT_HELPER2.read_text()
    )
    helper3_containers, helper3_statements = extract_from_parser(
        SCENIC_TEST_STRAIGHT_HELPER3.read_text()
    )

    assert [container.name for container in helper1_containers] == [
        "<initial>",
        "ImportedChain",
    ]
    assert [statement.container_name for statement in helper1_statements] == [
        "ImportedChain"
    ]
    assert helper1_statements[0].invocations[0].target == "Helper2Branch"

    assert [container.name for container in helper2_containers] == [
        "<initial>",
        "Helper2Branch",
    ]
    assert [statement.container_name for statement in helper2_statements] == [
        "Helper2Branch"
    ]
    assert helper2_statements[0].operator == "choose"
    assert [inv.target for inv in helper2_statements[0].invocations] == [
        "Helper3A",
        "Helper3B",
    ]
    assert [inv.weight for inv in helper2_statements[0].invocations] == [2.0, 1.0]

    assert [container.name for container in helper3_containers] == [
        "<initial>",
        "Helper3A",
        "Helper3B",
        "StraightLeaf",
    ]
    assert [statement.container_name for statement in helper3_statements] == [
        "Helper3A",
        "Helper3B",
    ]


def test_extract_from_parser_captures_case_scenario_main_and_helper():
    main_containers, main_statements = extract_from_parser(
        SCENIC_TEST_SCENARIO_MAIN.read_text()
    )
    helper_containers, helper_statements = extract_from_parser(
        SCENIC_TEST_SCENARIO_HELPER1.read_text()
    )

    assert [container.name for container in main_containers] == [
        "<initial>",
        "Main",
        "LocalScenario",
        "AlternateScenario",
        "LocalBehavior",
    ]
    assert [container.kind for container in main_containers] == [
        "initial",
        "scenario",
        "scenario",
        "scenario",
        "behavior",
    ]
    assert [statement.container_name for statement in main_statements] == [
        "Main",
        "Main",
        "LocalScenario",
        "AlternateScenario",
    ]
    assert [statement.operator for statement in main_statements] == [
        "parallel",
        "choose",
        "parallel",
        "parallel",
    ]
    assert [container.name for container in helper_containers] == [
        "<initial>",
        "ImportedBehavior",
        "ImportedScenario",
        "ImportedLeaf",
    ]
    assert [container.kind for container in helper_containers] == [
        "initial",
        "behavior",
        "scenario",
        "behavior",
    ]
    assert [statement.container_name for statement in helper_statements] == [
        "ImportedBehavior",
        "ImportedScenario",
    ]


def test_extract_from_parser_captures_interrupt_and_temporal_constructs():
    containers, statements = extract_from_parser(SCENIC_TEST_INTERRUPT_MAIN.read_text())

    assert [container.name for container in containers] == [
        "<initial>",
        "MainBehavior",
        "BaseBehavior",
        "InterruptBehavior",
        "TimedBehavior",
    ]
    assert [statement.node_id for statement in statements] == [
        "MainBehavior:1",
        "MainBehavior:2",
        "MainBehavior:3",
    ]
    assert [statement.operator for statement in statements] == [
        "parallel",
        "until",
        "for",
    ]
    assert statements[0].nesting == ("try",)
    assert statements[1].nesting == (
        "try",
        "interrupt when simulation().currentTime > 1",
    )
    assert statements[2].nesting == (
        "try",
        "interrupt when simulation().currentTime > 1",
    )
    assert [inv.target for inv in statements[1].invocations] == ["InterruptBehavior"]
    assert [inv.target for inv in statements[2].invocations] == ["TimedBehavior"]


def test_extract_from_parser_tolerates_monitor_require_case_and_collects_behaviors():
    containers, statements = extract_from_parser(SCENIC_TEST_MONITOR_MAIN.read_text())

    assert [container.name for container in containers] == [
        "<initial>",
        "MainBehavior",
        "BranchBehavior",
        "LeafA",
        "LeafB",
    ]
    assert [statement.container_name for statement in statements] == [
        "MainBehavior",
        "BranchBehavior",
    ]
    assert [statement.operator for statement in statements] == [
        "parallel",
        "choose",
    ]


def test_target_name_and_parse_weight_helpers():
    assert target_name("FollowLaneBehavior(speed)") == "FollowLaneBehavior"
    assert target_name("CollisionAvoidance()") == "CollisionAvoidance"
    assert target_name("vehicle + 1") is None

    assert parse_weight("3") == 3.0
    assert parse_weight("0.25") == 0.25
    assert parse_weight("not-a-number") is None
    assert target_name("WeightedA()") == "WeightedA"
    assert parse_weight("2.0") == 2.0


def test_operator_semantics_for_all_supported_operators():
    assert operator_semantics("parallel", "behavior") == {
        "container_kind": "behavior",
        "execution": "parallel-all",
        "randomized": False,
        "weighted": False,
    }
    assert operator_semantics("choose", "scenario") == {
        "container_kind": "scenario",
        "execution": "single-enabled-choice",
        "randomized": True,
        "weighted": True,
    }
    assert operator_semantics("shuffle", "scenario") == {
        "container_kind": "scenario",
        "execution": "random-permutation-of-enabled-choices",
        "randomized": True,
        "weighted": True,
    }
    assert operator_semantics("until", "behavior") == {
        "container_kind": "behavior",
        "execution": "parallel-all-until-condition",
        "randomized": False,
        "weighted": False,
    }
    assert operator_semantics("for", "behavior") == {
        "container_kind": "behavior",
        "execution": "parallel-all-for-duration",
        "randomized": False,
        "weighted": False,
    }


def test_dataclasses_round_trip_with_as_dict():
    graph = CompositionGraph(
        source_path="example.scenic",
        source_kind="path",
        container_names=("Main",),
        statements=(
            CompositionStatement(
                node_id="Main:1",
                container_name="Main",
                operator="parallel",
                semantics={"container_kind": "scenario"},
                invocations=(
                    InvocationSpec(
                        text="Sub()",
                        target="Sub",
                        weight=None,
                        is_weighted=False,
                        line=3,
                    ),
                ),
                line=3,
            ),
        ),
        nodes=(
            GraphNode(id="scenario:Main", kind="scenario", label="Main"),
            GraphNode(id="Main:1", kind="composition", label="parallel"),
        ),
        edges=(GraphEdge(source="scenario:Main", target="Main:1", kind="contains"),),
    )

    as_dict = graph.as_dict()

    assert as_dict["container_names"] == ("Main",)
    assert as_dict["statements"][0]["container_name"] == "Main"
    assert as_dict["nodes"][0]["id"] == "scenario:Main"
    assert as_dict["edges"][0]["kind"] == "contains"


def test_execution_and_sxo_dataclasses_round_trip_with_as_dict():
    node = GraphNode(id="behavior:Foo", kind="behavior", label="Foo")
    execution = ExecutionStructure(
        container_ids=("behavior:Foo",),
        containers={
            "behavior:Foo": {
                "node": node,
                "composition_ids": ["Foo:1"],
                "start_ids": ["Foo:1"],
            }
        },
        compositions={
            "Foo:1": {
                "node": GraphNode(id="Foo:1", kind="composition", label="parallel"),
                "invocation_ids": ["Foo:1:invocation:0"],
                "next_ids": [],
            }
        },
        invocations={
            "Foo:1:invocation:0": GraphNode(
                id="Foo:1:invocation:0", kind="invocation", label="Bar"
            )
        },
        node_by_id={"behavior:Foo": node},
    )
    sxo = SXOStructure(
        nodes=(SXONode(id="S:behavior:Foo", kind="S", label="Foo", attributes={}),),
        edges=(SxOEdge(source="S:behavior:Foo", target="X:Foo:1", kind="S_to_X", attributes={}),),
    )

    assert execution.as_dict()["container_ids"] == ("behavior:Foo",)
    assert execution.as_dict()["containers"]["behavior:Foo"]["node"]["label"] == "Foo"
    assert sxo.as_dict()["nodes"][0]["kind"] == "S"
    assert sxo.as_dict()["edges"][0]["kind"] == "S_to_X"


def test_sort_node_ids_orders_by_line_then_id():
    node_by_id = {
        "b": GraphNode(id="b", kind="composition", label="parallel", attributes={"line": 3}),
        "a": GraphNode(id="a", kind="composition", label="parallel", attributes={"line": 3}),
        "c": GraphNode(id="c", kind="composition", label="parallel", attributes={"line": 1}),
    }

    assert sort_node_ids(["b", "a", "c"], node_by_id) == ["c", "a", "b"]


def test_ordered_compositions_follows_start_and_next_then_remaining():
    execution = ExecutionStructure(
        container_ids=("behavior:Foo",),
        containers={
            "behavior:Foo": {
                "node": GraphNode(id="behavior:Foo", kind="behavior", label="Foo"),
                "composition_ids": ["Foo:1", "Foo:2", "Foo:3"],
                "start_ids": ["Foo:1"],
            }
        },
        compositions={
            "Foo:1": {
                "node": GraphNode(id="Foo:1", kind="composition", label="parallel"),
                "invocation_ids": [],
                "next_ids": ["Foo:2"],
            },
            "Foo:2": {
                "node": GraphNode(id="Foo:2", kind="composition", label="parallel"),
                "invocation_ids": [],
                "next_ids": [],
            },
            "Foo:3": {
                "node": GraphNode(id="Foo:3", kind="composition", label="parallel"),
                "invocation_ids": [],
                "next_ids": [],
            },
        },
        invocations={},
        node_by_id={},
    )

    ordered = ordered_compositions(execution.containers["behavior:Foo"], execution)

    assert ordered == ["Foo:1", "Foo:2", "Foo:3"]


def test_choose_invocation_prefers_weighted_choice(monkeypatch):
    invocation_nodes = {
        "a": GraphNode(id="a", kind="invocation", label="A", attributes={"weight": 1.0}),
        "b": GraphNode(id="b", kind="invocation", label="B", attributes={"weight": 5.0}),
    }

    def fake_choices(population, weights, k):
        assert population == ["a", "b"]
        assert weights == [1.0, 5.0]
        assert k == 1
        return ["b"]

    monkeypatch.setattr("tools.scenic_composition_analysis_helpers.random.choices", fake_choices)

    assert choose_invocation(["a", "b"], invocation_nodes) == "b"


def test_choose_invocation_uses_uniform_choice_without_weights(monkeypatch):
    invocation_nodes = {
        "a": GraphNode(id="a", kind="invocation", label="A", attributes={}),
        "b": GraphNode(id="b", kind="invocation", label="B", attributes={}),
    }

    monkeypatch.setattr("tools.scenic_composition_analysis_helpers.random.choice", lambda population: population[0])

    assert choose_invocation(["a", "b"], invocation_nodes) == "a"


def test_invocation_result_prefers_target_over_text():
    with_target = GraphNode(
        id="a",
        kind="invocation",
        label="A",
        attributes={"target": "CollisionAvoidance", "text": "CollisionAvoidance()"},
    )
    without_target = GraphNode(
        id="b",
        kind="invocation",
        label="B",
        attributes={"target": None, "text": "new Object"},
    )

    assert invocation_result(with_target) == "CollisionAvoidance"
    assert invocation_result(without_target) == "new Object"


def test_sample_composition_parallel_returns_all_targets():
    composition = {
        "node": GraphNode(id="Foo:1", kind="composition", label="parallel"),
        "invocation_ids": ["a", "b"],
    }
    invocations = {
        "a": GraphNode(id="a", kind="invocation", label="A", attributes={"target": "A"}),
        "b": GraphNode(id="b", kind="invocation", label="B", attributes={"target": "B"}),
    }

    assert sample_composition(composition, invocations) == ["A", "B"]


def test_sample_composition_choose_and_shuffle(monkeypatch):
    choose_composition = {
        "node": GraphNode(id="Foo:1", kind="composition", label="choose"),
        "invocation_ids": ["a", "b"],
    }
    shuffle_composition = {
        "node": GraphNode(id="Foo:2", kind="composition", label="shuffle"),
        "invocation_ids": ["a", "b"],
    }
    invocations = {
        "a": GraphNode(id="a", kind="invocation", label="A", attributes={"target": "A"}),
        "b": GraphNode(id="b", kind="invocation", label="B", attributes={"target": "B"}),
    }

    monkeypatch.setattr(
        "tools.scenic_composition_analysis_helpers.choose_invocation",
        lambda invocation_ids, invocation_nodes: "b",
    )
    monkeypatch.setattr(
        "tools.scenic_composition_analysis_helpers.random.shuffle",
        lambda items: items.reverse(),
    )

    assert sample_composition(choose_composition, invocations) == ["B"]
    assert sample_composition(shuffle_composition, invocations) == ["B", "A"]
