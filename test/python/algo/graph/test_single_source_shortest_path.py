import pprint

from src.python.algo.graph.SingleSourceShortestPath import SingleSourceShortestPath


def test_dijkstra_algorithm():
    sssp = SingleSourceShortestPath()
    res = sssp.dijkstra_algorithm()
    pprint.pprint(res)
    assert (res == {'A': 0, 'B': 1, 'C': 1, 'D': 2, 'E': 2})
