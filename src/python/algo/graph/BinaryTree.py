import collections
from typing import List, Optional


class TreeNode:
    def __init__(self, val: int = None):
        self.left: Optional["TreeNode"] = None
        self.right: Optional["TreeNode"] = None
        self.val: int = val


class BinaryTreeTraversal:

    @staticmethod
    def dfs_inorder(root: TreeNode) -> List[int]:
        # method-1: with recursion
        # if not root: return []
        # return  BinaryTreeTraversal.dfs_preorder(root.left) + [root.val] + BinaryTreeTraversal.dfs_preorder(root.right)

        # method-2: with iteration
        node = root
        stack = []
        res = []
        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            res.append(node.val)
            node = node.right
        return res

    @staticmethod
    def dfs_preorder(root: TreeNode) -> List[int]:
        # method-1: recursion
        # if not root: return []
        # return [root.val] + BinaryTreeTraversal.dfs_preorder(root.left) + BinaryTreeTraversal.dfs_preorder(root.right)

        # method-2: stack
        if not root: return []
        res = []
        stack = [root]
        while stack:
            node = stack.pop()
            res.append(node.val)
            if node.right: stack.append(node.right)
            if node.left: stack.append(node.left)
        return res

    @staticmethod
    def dfs_postorder(root: TreeNode) -> List[int]:
        if not root: return []
        return BinaryTreeTraversal.dfs_postorder(root.left) + BinaryTreeTraversal.dfs_postorder(root.right) + [root.val]

    @staticmethod
    def bfs(root: TreeNode) -> List[int]:
        if not root: return []
        res = []
        queue = collections.deque([root])
        while queue:
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
            res.append(node.val)
        return res

    @staticmethod
    def moriss_inorder(root: TreeNode) -> List[int]:
        res = []
        curr_node = root
        while curr_node:

            if curr_node.left:

                # find predecessor
                predecessor = curr_node.left
                while predecessor.right and predecessor.right != curr_node:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # build the link from predecessor to curr_node
                    predecessor.right = curr_node
                    curr_node = curr_node.left
                else:
                    # has visited, break the link
                    res.append(curr_node.val)
                    predecessor.right = None
                    curr_node = curr_node.right

            else:
                res.append(curr_node.val)
                curr_node = curr_node.right

        return res


if __name__ == "__main__":
    """
        1
    2      3
   4  5      6
   
   in order: 4 2 5 1 3 6
    """
    n1 = TreeNode(1)
    n2 = TreeNode(2)
    n3 = TreeNode(3)
    n4 = TreeNode(4)
    n5 = TreeNode(5)
    n6 = TreeNode(6)
    n1.left = n2
    n1.right = n3
    n2.left = n4
    n2.right = n5
    n3.right = n6

    exp_res_preorder = [1, 2, 4, 5, 3, 6]
    exp_res_inorder = [4, 2, 5, 1, 3, 6]
    exp_res_postorder = [4, 5, 2, 6, 3, 1]
    exp_res_level = [1, 2, 3, 4, 5, 6]
    assert (exp_res_inorder == BinaryTreeTraversal.moriss_inorder(n1))
    print(BinaryTreeTraversal.moriss_inorder(n1))

    assert (exp_res_inorder == BinaryTreeTraversal.dfs_inorder(n1))
    print(BinaryTreeTraversal.dfs_inorder(n1))

    assert (exp_res_postorder == BinaryTreeTraversal.dfs_postorder(n1))
    print(BinaryTreeTraversal.dfs_postorder(n1))

    assert (exp_res_level == BinaryTreeTraversal.bfs(n1))
    print(BinaryTreeTraversal.bfs(n1))
