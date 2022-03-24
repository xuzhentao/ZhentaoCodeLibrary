import collections
from typing import List


class DisjointSet:
    # Helper function to print the disjoint set.
    def __str__(self):
        s = set(range(self.size))
        mapRoottoNum = collections.defaultdict(list)
        while s:
            e = list(s)[0]
            mapRoottoNum[self.find(e)].append(e)
            s.remove(e)
        res = "Disjoint Set:\n"
        ctr = 0
        for k, v in mapRoottoNum.items():
            res += "Group [" + str(ctr) + "]:" + " - ".join([str(x) for x in v]) + "\n"
            ctr += 1
        return res


class DisjointSetQuickFind(DisjointSet):

    def __init__(self, size):
        # the rootest parent for corresponding note.
        self.root = [i for i in range(size)]
        self.size = size

    # only one layers, just return the parent.
    def find(self, x):
        return self.root[x]

    # iterate through the entire node list, and manually move the node belonging to xRoot to yRoot.
    def union(self, x, y):
        # find the root to check if are the same set.
        xRoot: int = self.find(x)
        yRoot: int = self.find(y)
        if xRoot != yRoot:
            for i in range(self.size):
                if self.find(i) == xRoot:
                    self.root[i] = yRoot


class DisjointSetQuickUnion(DisjointSet):
    def __init__(self, size):
        self.parents = [i for i in range(size)]
        self.size = size

    def find(self, x):
        # keep finding the parent until the end.
        while x != self.parents[x]:
            x = self.parents[x]
        return x

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot != yRoot:
            self.parents[xRoot] = yRoot


class DisjointSetUnionWithRank(DisjointSet):
    def __init__(self, size):
        self.parents = [i for i in range(size)]
        # rank means the height of a node.
        self.rank = [1] * size
        # self.size = size

    def find(self, x):
        while x != self.parents[x]:
            x = self.parents[x]
        return x

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot != yRoot:
            if self.rank[x] > self.rank[y]:
                self.parents[yRoot] = xRoot
            elif self.rank[x] < self.rank[y]:
                self.parents[xRoot] = yRoot
            else:
                self.parents[xRoot] = yRoot
                self.rank[yRoot] += 1


# Leetcode highly recommend us to memorize this optimization method, which is almost O(1) for any find or union
# operation.
class DisjointSetUnionwithRankandPathCompression(DisjointSet):
    def __init__(self, size):
        self.parents = [i for i in range(size)]
        self.rank = [1] * size
        self.size = size
        # self.numComponents = size

    def find(self, x) -> int:
        # terminal condition
        if x == self.parents[x]:
            return x
        # 递归寻找parent，把最终的parent作为当前x的parent
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot != yRoot:
            # self.numComponents -= 1
            if self.rank[x] > self.rank[y]:
                self.parents[yRoot] = xRoot
            elif self.rank[x] < self.rank[y]:
                self.parents[xRoot] = yRoot
            else:
                self.parents[xRoot] = yRoot
                self.rank[yRoot] += 1

    # def getNumComponents(self):
    #     return self.numComponents
    #
    # def getComponents(self) -> List[List[int]]:
    #     s = set(range(self.size))
    #     mapRoottoNum = collections.defaultdict(list)
    #     while s:
    #         e = list(s)[0]
    #         mapRoottoNum[self.find(e)].append(e)
    #         s.remove(e)
    #     return list(mapRoottoNum.values())


if __name__ == "__main__":
    dj = DisjointSetUnionwithRankandPathCompression(10)
    print(dj)
    print(dj.getComponents())

    dj.union(1, 3)
    print(dj)
    print(dj.getComponents())


    dj.union(2, 4)
    print(dj)
    print(dj.getComponents())


    dj.union(1, 4)
    print(dj)
    print(dj.getComponents())