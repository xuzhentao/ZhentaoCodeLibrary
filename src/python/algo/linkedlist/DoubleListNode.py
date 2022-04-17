from typing import *


class DoubleListNode:
    def __init__(self, key: int, val: int, name: str = None):
        self.key: int = key
        self.val: int = val
        self.prev: DoubleListNode = None
        self.next: DoubleListNode = None
        self.name: Optional[str] = name

    def __str__(self):

        res = "DoubleListNode("
        if self.name:
            res += "Name=" + str(self.name) + ","
        res += " key = " + str(self.key) + ", value = " + str(self.val) + ")"
        if self.next:
            res += " --> " + self.next.__str__()
        return res
