import networkx as nx
import pytest

from resilientim.graph import make_synthetic_graph


def test_synthetic_graph_has_complete_disjoint_community_partition():
    graph = make_synthetic_graph(3, 4, 0.0, 0.0, seed=13)

    assert graph.number_of_nodes() == 12
    assert graph.number_of_edges() == 0  # Isolated nodes must not disappear.
    communities = [graph.nodes[node]["community"] for node in graph]
    assert set(communities) == {0, 1, 2}
    assert all(communities.count(community) == 4 for community in range(3))


def test_synthetic_graph_is_reproducible_and_does_not_change_global_rng():
    import random

    random.seed(99)
    expected_next_value = random.Random(99).random()
    first = make_synthetic_graph(2, 5, 0.4, 0.2, seed=7)
    observed_next_value = random.random()
    second = make_synthetic_graph(2, 5, 0.4, 0.2, seed=7)

    assert set(first.edges) == set(second.edges)
    assert observed_next_value == expected_next_value


def test_probability_extremes_create_expected_directed_edges():
    graph = make_synthetic_graph(2, 2, 1.0, 0.0, seed=1)

    assert nx.number_of_selfloops(graph) == 0
    assert graph.number_of_edges() == 4
    assert all(graph.nodes[source]["community"] == graph.nodes[target]["community"]
               for source, target in graph.edges)


@pytest.mark.parametrize(
    "arguments",
    [
        (0, 2, 0.1, 0.1, 1),
        (2, 0, 0.1, 0.1, 1),
        (2, 2, -0.1, 0.1, 1),
        (2, 2, 0.1, 1.1, 1),
    ],
)
def test_invalid_generator_parameters_are_rejected(arguments):
    with pytest.raises(ValueError):
        make_synthetic_graph(*arguments)
