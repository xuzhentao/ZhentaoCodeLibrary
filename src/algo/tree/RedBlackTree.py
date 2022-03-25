from enum import Enum
from typing import Any


# Edge Color Enumeration
class Color(Enum):
    RED = "RED"
    BLACK = "BLACK"


class RedBlackTreeNode:

    def __init__(self, key: Any, val: Any, color=Color.BLACK):
        self.left: RedBlackTreeNode = None
        self.right: RedBlackTreeNode = None
        self.color: Color = color
        self.key: Any = key
        self.val: Any = val

    @staticmethod
    def put(node: "RedBlackTreeNode", key: Any, val: Any):
        """
        Insert node(key, val) into a tree with root node
        :param node: tree root
        :param key:
        :param val:
        :return:
        """
        if node is None:
            return RedBlackTreeNode(key, val, Color.RED)
        # overwrite key value pair
        elif node.key == key:
            node.val = val

        # insert into left child path
        elif node.key < key:
            node.right = RedBlackTreeNode.put(node.right, key, val)

        # insert into right child path
        else:
            node.left = RedBlackTreeNode.put(node.left, key, val)

        # 以下代卖的顺序不能变，因为变换分三种，前者会变成后者。
        if RedBlackTreeNode._is_red(node.right) and not RedBlackTreeNode._is_red(node.left):
            node = RedBlackTreeNode._rotate_left(node)
        if node.left is not None and RedBlackTreeNode._is_red(node.left) and RedBlackTreeNode._is_red(node.left.left):
            node = RedBlackTreeNode._rotate_right(node)
        if RedBlackTreeNode._is_red(node.left) and RedBlackTreeNode._is_red(node.right):
            RedBlackTreeNode._flip_colors(node)
        return node

    @staticmethod
    def find(node, key) -> Any:
        if node is None:
            return None
        if node.key == key:
            return node.val
        elif key < node.key:
            return RedBlackTreeNode.find(node.left, key)
        else:
            return RedBlackTreeNode.find(node.right, key)

    @staticmethod
    def _is_red(node: "RedBlackTreeNode"):
        if node is None: return False  # null link is black
        return node.color == Color.RED

    def print(self, ind: int = 0):
        for _ in range(ind):
            print("-", end="")
        print("[" + self.color.value + ']' + str(self.key) + "-->" + str(self.val))
        if self.left is not None:
            self.left.print(ind + 1)
        if self.right is not None:
            self.right.print(ind + 1)

    @staticmethod
    def _rotate_left(node):
        """
               node
             |       |
             l       node_right
                     |        |
                    m        r

            is rotated to

                     node_right
                     |        |
                    node        r
                    |   |
                    l   m
        :param node:
        :return:
        """
        assert (node.right is not None)
        node_right = node.right
        # change color
        node.color, node_right.color = node_right.color, node.color
        # change link
        node.right, node_right.left = node_right.left, node
        return node_right

    @staticmethod
    def _rotate_right(node):
        """

                     node
                     |               |
                    node_left        r
                    |   |
                    l   m

            is rotated to

                     node_left
                     |       |
                    l        node
                            |   |
                            m   r
        :param node:
        :return:
        """
        node_left = node.left
        # switch color
        node.color, node_left.color = node_left.color, node.color
        node.left, node_left.right = node_left.right, node
        return node_left

    @staticmethod
    def _flip_colors(node):
        assert (node.left.color == Color.RED)
        assert (node.right.color == Color.RED)
        assert (node.color == Color.BLACK)
        node.left.color = Color.BLACK
        node.right.color = Color.BLACK
        node.color = Color.RED


class RedBlackTree:

    def __init__(self):
        self.root = None

    def insert(self, key, val):
        self.root = RedBlackTreeNode.put(self.root, key, val)

    def find(self, key: Any) -> Any:
        return RedBlackTreeNode.find(self.root, key)

    def print(self):
        print("\n=============Red Black Tree===========")
        print(self.root.print(0))
        print("======================================")
