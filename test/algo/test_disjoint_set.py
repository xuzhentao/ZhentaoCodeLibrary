from algo.graph.DisjointSet import DisjointSetQuickFind


def test_disjoint_set_quick_find():
    dj = DisjointSetQuickFind(10)
    print(dj)
    dj.union(1, 3)
    print(dj)
    dj.union(2, 4)
    print(dj)
    assert (dj.root == [0, 3, 4, 3, 4, 5, 6, 7, 8, 9])


if __name__ == "__main__":
    test_disjoint_set_quick_find()
