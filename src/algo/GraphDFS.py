from typing import *


class GraphDFS:

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

    def find_all_node_in_graph_wih_dfs(self, starting_node="A"):
        stack: List[str] = [starting_node]
        visited: Set[str] = set()
        print("initial status, stack = " + str(stack))
        while stack:
            print("stack = " + str(stack) + "; visited = " + str(visited))
            node = stack.pop()
            print("\tpopped node " + node)

            if node not in visited:
                visited.add(node)
                print("\tode " + node + " visited")
                for neighbor in self.g[node]:
                    stack.append(neighbor)
                print("\tnodes " + str(self.g[node]) + " added to the stack")
        return visited

    def find_all_path_between_two_nodes(self, starting_node: str = "A", ending_node: str = "B"):

        stack: List[List[str]] = []
        res: List[List[str]] = []
        for starting_neighbors in self.g[starting_node]:
            stack.append([starting_node, starting_neighbors])
        print("initial stack = " + str(stack))
        while stack:
            print("stack status = " + str(stack))
            edge: List[str] = stack.pop()
            last_node: str = edge[-1]

            # path found
            if last_node == ending_node:
                res.append(edge)

            visited: Set[str] = set(edge)
            for last_node_neighbor in self.g[last_node]:
                if last_node_neighbor not in visited:
                    stack.append(edge[:] + [last_node_neighbor])

        return res

    def find_all_path_between_two_nodes_with_backtracking(self, starting_node: str = "A", ending_node: str = "B"):

        result: List[List[str]] = []

        def backtracking(curr_node: str, path: List[str], visited: Set[str]) -> None:
            print("curr_node = " + curr_node + "; path = " + str(path) + "; visited = " + str(visited))
            if curr_node == ending_node:
                result.append(path[:])
                print("\tfound " + str(path))
                return

            for neighbor_node in self.g[curr_node]:
                if neighbor_node not in visited:
                    visited.add(neighbor_node)
                    path.append(neighbor_node)
                    backtracking(neighbor_node, path, visited)
                    visited.remove(neighbor_node)
                    path.pop()

        backtracking(starting_node, [starting_node], {starting_node})
        return result


if __name__ == "__main__":
    dfsingraph = GraphDFS()
    # print(dfsingraph.find_all_node_in_graph_wih_dfs())
    print(dfsingraph.find_all_path_between_two_nodes_with_backtracking())
