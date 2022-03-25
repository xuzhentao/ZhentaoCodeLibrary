######################################################################################
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2022/3/24
#	Description: 			BFS in Graph
#	Tested Environment:		Macbook Pro w/ Python 3.9
#	Required Libraries:		N/A
######################################################################################

from typing import *


class GraphBFS:

    def __init__(self):
        self.g: Dict[str, List[str]] = dict()
        self.generate_sample_data()

    def generate_sample_data(self):
        """
        A ----B--\
        | \   |   \
        C  D  |   F
        |   \ |  /
        |-----E/
        """
        self.g: Dict[str, List[str]] = {"A": ["C", "B", "D"], "B": ["A", "E", "F"], "C": ["A", "E"], "D": ["A", "E"],
                                        "E": ["B", "C", "D", "F"], "F": ["B", "E"]}

    def find_shortest_path_between_two_nodes(self, starting_node="A", end_node="B"):

        from collections import deque
        queue = deque([[starting_node]])
        visited: Set[str] = {starting_node}

        print("initial queue = " + str(queue))

        while queue:
            print("queue status = " + str(queue))
            path = queue.popleft()
            curr_node = path[-1]

            print("\tthe path to handle = " + str(path) + " with last element " + curr_node)

            if curr_node == end_node:
                return path

            for neighbor in self.g[curr_node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path[:] + [neighbor])


if __name__ == "__main__":
    dfsingraph = GraphBFS()
    print(dfsingraph.find_shortest_path_between_two_nodes("C", "B"))
