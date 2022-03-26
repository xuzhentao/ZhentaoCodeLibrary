import pprint

from src.python.algo.graph.SingleSourceShortestPath import SingleSourceShortestPath


def test_dijkstra_algorithm():
    sssp = SingleSourceShortestPath()
    res = sssp.dijkstra_algorithm(sssp.graph)
    pprint.pprint(res)
    assert (res == {'A': (0, '-'), 'B': (1, 'A'), 'C': (1, 'A'), 'D': (2, 'C'), 'E': (2, 'B')})


def test_bellman_ford_algorithm():
    sssp = SingleSourceShortestPath()
    res = sssp.bellman_ford_algorithm(sssp.graph)
    pprint.pprint(res)
    assert (res == {'A': (0, '-'), 'B': (1, 'A'), 'C': (1, 'A'), 'D': (2, 'C'), 'E': (2, 'B')})


def test_bellman_ford_algorithm_neg():
    sssp = SingleSourceShortestPath()
    res = sssp.bellman_ford_algorithm(sssp.graph_neg)
    pprint.pprint(res)
    assert (res == {'A': (0, '-'), 'B': (50, 'D'), 'C': (150, 'B'), 'D': (200, 'A')})
