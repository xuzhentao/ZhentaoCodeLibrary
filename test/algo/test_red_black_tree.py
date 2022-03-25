# from src.algo.RedBlackTree import RedBlackTree, Color
#
#
# def test_insert():
#     rbt = RedBlackTree()
#     rbt.insert(1, None)
#     rbt.insert(2, 2)
#     rbt.insert(3, None)
#     rbt.insert(0, None)
#     rbt.insert(0.5, None)
#     assert (rbt.root.color == Color.RED)
#     assert (rbt.root.key == 2)
#     assert (rbt.root.left.color == Color.RED)
#     assert (rbt.root.left.key == 0.5)
#
#     assert (2, rbt.find(2))
#     assert (None, rbt.find(-1))
#
#
# if __name__ == "__main__":
#     test_insert()
