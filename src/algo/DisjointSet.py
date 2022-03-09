import collections


class DisjointSet:
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
        self.root = [i for i in range(size)]
        self.size = size

    def find(self, x):
        return self.root[x]

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot != yRoot:
            for i in range(self.size):
                if self.find(i) == xRoot:
                    self.root[i] = yRoot


class DisjointSetQuickUnion(DisjointSet):
    def __init__(self, size):
        self.parents = [i for i in range(size)]
        self.size = size

    def find(self, x):
        while x != self.parents[x]:
            x = self.parents[x]
        return x

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot != yRoot:
            self.parents[xRoot] = yRoot

class DisjointSetUnionwithRank(DisjointSet):
    def __init__(self, size):
        self.parents = [i for i in range(size)]
        self.rank = [1] * size
        self.size = size

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




if __name__ == "__main__":
    dj = DisjointSetUnionwithRank(10)
    print(dj)

    dj.union(1, 3)
    print(dj)

    dj.union(2, 4)
    print(dj)

    dj.union(1, 5)
    print(dj)

    dj.union(9, 5)
    print(dj)

    dj.union(9, 2)
    print(dj)

    dj.union(7, 8)
    print(dj)

    dj.union(7, 6)
    print(dj)

    dj.union(1, 6)
    print(dj)

    dj.union(1, 0)
    print(dj)
