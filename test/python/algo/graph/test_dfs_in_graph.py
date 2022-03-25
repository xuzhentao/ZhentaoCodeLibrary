from src.python.algo.graph.GraphDFS import GraphDFS


def test_find_all_node_in_graph_wih_dfs():
    dfsingraph = GraphDFS()
    res = dfsingraph.find_all_node_in_graph_wih_dfs()
    assert (res == {"A", "B", "C", "D", "E", "F"})


if __name__ == "__main__":
    res = test_find_all_node_in_graph_wih_dfs()
