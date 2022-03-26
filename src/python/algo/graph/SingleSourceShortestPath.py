######################################################################################
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2022/3/24
#	Description: 			Single Source The Shortest Path in Graph
#	Tested Environment:		Macbook Pro w/ Python 3.9
#	Required Libraries:		N/A
######################################################################################
import collections
import heapq
import pprint
import sys
from typing import *


def helper_visualize_shortest_path_result(d: Dict[str, Tuple[int, str]]) -> None:
    for node in d:
        path = [node]
        while d[path[-1]][1] != '-':
            path.append(d[path[-1]][1])
        print(
            "node = " + node + "\t shortest_distance = " + str(d[node][0]) + "\t path from source = " + str(path[::-1]))


class SingleSourceShortestPath:

    def __init__(self):
        # graph: key is vertex, value is vertex and corresponding weight.
        self.graph: Dict[str, List[Tuple[str, int]]] = {"A": [("B", 1), ("C", 1), ("D", 3)],
                                                        "B": [("A", 1), ("D", 2), ("E", 1)], "C": [("A", 1), ("D", 1)],
                                                        "D": [("C", 1), ("A", 3), ("B", 2), ("E", 2)],
                                                        "E": [("B", 1), ("D", 2)]}

        self.graph_neg: Dict[str, List[Tuple[str, int]]] = {"A": [("B", 100), ("C", 500), ("D", 200)],
                                                            "B": [("C", 100)], "C": [("D", 100)], "D": [("B", -150)]}

    def dijkstra_algorithm(self, graph, starting_point: str = "A") -> Dict[str, Tuple[int, str]]:
        """
        pre-requist: the graph has NO negative value weights.
        find the shortest path from starting_point to all points.
        Time complexity: O((v+e)logv) #
        :return: a distance dictionary for all vertex with minimal distance from starting_point to each vertex.
        """
        dist: Dict[str, Tuple[int, str]] = {k: (sys.maxsize, None) for k in
                                            graph.keys()}  # the second element is the parent.
        dist[starting_point] = (0, "-")

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
            for neighbor_node, neighbor_dist in graph[curr_node]:
                if neighbor_node is S:
                    continue
                print("\tcomparing the current distance " + str(
                    dist[neighbor_node]) + " and the potentially shorter distance from curr_node " + str(
                    curr_node) + " and neighbor " + str(neighbor_node) + " with distance " + str(
                    neighbor_dist + curr_dist))
                if neighbor_dist + curr_dist < dist[neighbor_node][0]:
                    dist[neighbor_node] = (neighbor_dist + curr_dist, curr_node)
                    heapq.heappush(Q, (dist[neighbor_node][0], neighbor_node))
                    print("\t\tshorter distance founded, added the node " + str(neighbor_node) + " to the heapq")
                else:
                    print("\t\tkeep the current dist")

        helper_visualize_shortest_path_result(dist)
        return dist

    def bellman_ford_algorithm(self, graph: Dict[str, List[Tuple[str, int]]]):
        """
        Algorithm introduction links: https://leetcode.com/explore/learn/card/graph/622/single-source-shortest-path-algorithm/3864/

        Algorithm complexity = O(V * E) because the number iteration is V and every time all the edge need to be
        traversed to update the corresponding destination value.
        :param graph:
        :return:
        """
        import numpy as np
        np.set_printoptions(linewidth=np.inf)

        def print_dp(dp):
            import copy
            dp_cp = copy.deepcopy(dp)
            for i in range(len(dp_cp)):
                for j in range(len(dp_cp[0])):
                    dp_cp[i][j] = str(dp_cp[i][j])
            print(np.array(dp_cp))

        # simple conversion on node name from str to int
        map_node_to_idx = {n: i for i, n in enumerate(sorted(graph.keys()))}
        graph: Dict[int, Dict[int, int]] = {map_node_to_idx[k]: {map_node_to_idx[k1]: v1 for k1, v1 in v} for k, v in
                                            graph.items()}
        n_node = len(graph)
        edges: List[Tuple[int, int, int]] = [(s, t, d) for s in graph.keys() for t, d in graph[s].items()]

        # step-2 initialize the DP table
        # row - i is the maximum used edge, column - j is the target to reach node j
        dp: List[List[(int, int)]] = [[(sys.maxsize, None)] * n_node for _ in range(n_node)]
        for i in range(n_node):
            dp[i][0] = (0, None)
        print("initial DP = ")
        print_dp(dp)

        # step 3, DP
        for i in range(1, n_node):
            print("=======Iteration = " + str(i) + "===========")
            for s, t, d in edges:
                print('processing edge from ' + str(s) + " to " + str(t) + " with weight " + str(d))
                if dp[i][t][0] > dp[i - 1][s][0] + graph[s][t]:
                    print("updating")
                    dp[i][t] = (dp[i - 1][s][0] + graph[s][t], s)
                print_dp(dp)

        dist = dict()
        map_idx_to_node = {v: k for k, v in map_node_to_idx.items()}
        for t, dist_p in enumerate(dp[-1]):
            dist[map_idx_to_node[t]] = (dist_p[0], map_idx_to_node[dist_p[1]] if dist_p[1] is not None else '-')
        helper_visualize_shortest_path_result(dist)
        return dist

    def improved_bellman_ford_algorithm(self, graph: Dict[str, List[Tuple[str, int]]]):

        import numpy as np
        np.set_printoptions(linewidth=np.inf)

        def print_dp(dp):
            import copy
            dp_cp = copy.deepcopy(dp)
            for i in range(len(dp_cp)):
                for j in range(len(dp_cp[0])):
                    dp_cp[i][j] = str(dp_cp[i][j])
            print(np.array(dp_cp))

        # simple conversion on node name from str to int
        map_node_to_idx = {n: i for i, n in enumerate(sorted(graph.keys()))}
        graph: Dict[int, Dict[int, int]] = {map_node_to_idx[k]: {map_node_to_idx[k1]: v1 for k1, v1 in v} for k, v in
                                            graph.items()}
        n_node = len(graph)
        queue = collections.deque([0])
        dist: Dict[int, (int, int)] = {k: (sys.maxsize, None) for k in range(len(graph))}
        dist[0] = (0, None)
        visited: Set[int] = {0}

        while queue:
            node = queue.popleft()
            visited.remove(node)
            for target in graph[node].keys():

                if dist[target][0] > dist[node][0] + graph[node][target]:
                    if target not in visited:
                        visited.add(target)
                        queue.append(target)
                    dist[target] = (dist[node][0] + graph[node][target], node)

        map_idx_to_node = {v: k for k, v in map_node_to_idx.items()}
        dist_res = dict()
        for t, dist_p in list(dist.items()):
            dist_res[map_idx_to_node[t]] = (dist_p[0], map_idx_to_node[dist_p[1]] if dist_p[1] is not None else '-')
        helper_visualize_shortest_path_result(dist_res)

        print(dist_res)
        return dist_res


if __name__ == "__main__":
    sssp = SingleSourceShortestPath()
    # pprint.pprint(sssp.dijkstra_algorithm(graph=sssp.graph))
    pprint.pprint(sssp.bellman_ford_algorithm(graph=sssp.graph_neg))
    pprint.pprint(sssp.improved_bellman_ford_algorithm(graph=sssp.graph))
