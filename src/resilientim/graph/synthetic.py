"""Small reproducible synthetic graph generators used by experiments and examples."""

from __future__ import annotations

import random

import networkx as nx


def make_synthetic_graph(
    num_communities: int,
    nodes_per_community: int,
    within_community_probability: float,
    cross_community_probability: float,
    seed: int,
) -> nx.DiGraph:
    """Create a directed stochastic block graph with an explicit community partition.

    Nodes are labeled by consecutive integers. Every possible non-self directed edge is
    considered independently, using the within-community probability for endpoints in
    the same community and the cross-community probability otherwise. A local
    ``random.Random`` instance makes the result reproducible without changing global
    random state. Isolated nodes are retained.

    This function generates graph topology only; edge attributes for IC activation
    probabilities are deliberately not assigned.

    Args:
        num_communities: Positive number of disjoint communities.
        nodes_per_community: Positive, equal size for each community.
        within_community_probability: Edge probability in [0, 1] within a community.
        cross_community_probability: Edge probability in [0, 1] between communities.
        seed: Integer seed for the local pseudorandom generator.

    Returns:
        A directed NetworkX graph with node attribute ``community`` and graph metadata
        describing the generator parameters.

    Raises:
        ValueError: If a community count/size is not positive or a probability is out
            of range.
        TypeError: If ``seed`` is not an integer.
    """
    if num_communities <= 0:
        raise ValueError("num_communities must be positive")
    if nodes_per_community <= 0:
        raise ValueError("nodes_per_community must be positive")
    for name, probability in (
        ("within_community_probability", within_community_probability),
        ("cross_community_probability", cross_community_probability),
    ):
        if not 0.0 <= probability <= 1.0:
            raise ValueError(f"{name} must be in [0, 1]")
    if not isinstance(seed, int):
        raise TypeError("seed must be an integer")

    graph = nx.DiGraph(
        generator="directed_stochastic_block",
        seed=seed,
        num_communities=num_communities,
        nodes_per_community=nodes_per_community,
        within_community_probability=within_community_probability,
        cross_community_probability=cross_community_probability,
    )
    community_of = {}
    for community in range(num_communities):
        start = community * nodes_per_community
        for node in range(start, start + nodes_per_community):
            community_of[node] = community
            graph.add_node(node, community=community)

    rng = random.Random(seed)
    nodes = list(graph.nodes)
    for source in nodes:
        for target in nodes:
            if source == target:
                continue
            probability = (
                within_community_probability
                if community_of[source] == community_of[target]
                else cross_community_probability
            )
            if rng.random() < probability:
                graph.add_edge(source, target)
    return graph
