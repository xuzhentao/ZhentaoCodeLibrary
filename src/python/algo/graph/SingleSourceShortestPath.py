######################################################################################
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2022/3/24
#	Description: 			Single Source Shortest Path in Graph
#	Tested Environment:		Macbook Pro w/ Python 3.9
#	Required Libraries:		N/A
######################################################################################


import heapq
import pprint
import sys
from typing import *


class SingleSourceShortestPath:

    def __init__(self):
        # graph: key is vertex, value is vertex and corresponding weight.
        self.graph: Dict[str, List[Tuple[str, int]]] = {"A": [("B", 1), ("C", 1), ("D", 3)],
                                                        "B": [("A", 1), ("D", 2), ("E", 1)], "C": [("A", 1), ("D", 1)],
                                                        "D": [("C", 1), ("A", 3), ("B", 2), ("E", 2)],
                                                        "E": [("B", 1), ("D", 2)]}

    def dijkstra_algorithm(self, starting_point: str = "A") -> Dict[str, int]:
        """
        :return: a distance dictionary for all vertex with minimal distance from starting_point to each vertex.
        """
        dist: Dict[str, int] = {k: sys.maxsize for k in self.graph.keys()}
        dist[starting_point] = 0

        S: Set[str] = set()
        Q: List[Tuple[int, str]] = [(0, starting_point)]
        heapq.heapify(Q)

        print("initial heap queue = " + str(Q))
        while Q:
            print("heap queue = " + str(Q))
            print("\t dist = " + str(dist))
            curr_dist, curr_node = heapq.heappop(Q)
            print("\t popped node and its distance = " + str(curr_node) + " dist = " + str(curr_dist))
            S.add(curr_node)
            for neighbor_node, neighbor_dist in self.graph[curr_node]:
                if neighbor_node is S:
                    continue
                print("\tcomparing the current distance " + str(
                    dist[neighbor_node]) + " and the potentially shorter distance from curr_node " + str(
                    curr_node) + " and neighbor " + str(neighbor_node) + " with distance " + str(
                    neighbor_dist + curr_dist))
                if neighbor_dist + curr_dist < dist[neighbor_node]:
                    dist[neighbor_node] = neighbor_dist + curr_dist
                    heapq.heappush(Q, (dist[neighbor_node], neighbor_node))
                    print("\t\tshorter distance founded, added the node " + str(neighbor_node) + " to the heapq")
                else:
                    print("\t\tkeep the current dist")

        return dist


if __name__ == "__main__":
    sssp = SingleSourceShortestPath()
    pprint.pprint(sssp.dijkstra_algorithm())
