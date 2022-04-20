######################################################################################
#	Class: 					LFUCache
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2022/4/15
#	Description: 			Implement the LRU Cache.
#	Tested Environment:		Macbook pro w/ Python 3.9
######################################################################################

from typing import *

DUMMY_VALUE = -1


class DoubleListNode:

    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None
        self.freq: int = 1

    def __str__(self):
        return "DLN(key=" + str(self.key) + ", val = " + str(self.val) + ", freq = " + str(self.freq) + ")" + (
            ("-->" + str(self.next)) if self.next else "")


class DLL:

    def __str__(self):
        return "DLL(size=" + str(self.size) + ", content = {" + str(self.head) + "}" + ")"

    def __init__(self):
        self.head = DoubleListNode(0, 0)
        self.tail = DoubleListNode(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head
        self.size = 0

    def add_node_to_head(self, node: DoubleListNode) -> None:
        prev = node
        next = self.head.next
        prev.next, next.prev = next, prev

        prev = self.head
        next = node
        prev.next, next.prev = next, prev

        self.size += 1

    def remove_node_from_tail(self) -> DoubleListNode:
        if self.size == 0:
            print("Error in removing, DLL size = 0 already, can't remove from tail")
            return None
        node_to_remove = self.tail.prev
        prev = self.tail.prev.prev
        next = self.tail
        prev.next, next.prev = next, prev
        self.size -= 1
        return node_to_remove

    def remove_node(self, node: DoubleListNode):
        self.size -= 1
        prev = node.prev
        next = node.next
        prev.next, next.prev = next, prev
        return


class LFUCache:

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.cache: Dict[int, DLL] = {1: DLL()}  # map from frequency to dll, this can ensure the Frequency in LFU.
        self.map_key_to_node: Dict[int, DoubleListNode] = dict()  # this can quickly from key to node
        self.size = 0
        self.min_freq = 1

    def __str__(self):
        res = "=======LFUCache=========" + "\n"
        res += "size = " + str(self.size) + "\n"
        res += "min_freq = " + str(self.min_freq) + "\n"
        res += "capacity = " + str(self.capacity) + "\n"
        res += "frequency_map = " + str({k: str(v) for k, v in self.cache.items()}) + "\n"
        res += "key_node_map = " + str(
            {k: str(v.key) + ":" + str(v.val) + ":" + str(v.freq) for k, v in self.map_key_to_node.items()}) + "\n"
        res += "======================="
        return res

    def put(self, key: int, val: int):

        # edge case.
        if self.capacity == 0: return

        if key not in self.map_key_to_node:
            node = DoubleListNode(key, val)
            self.map_key_to_node[key] = node
            self.size += 1
            if self.size > self.capacity:
                self.size -= 1
                node_remove = self.cache[self.min_freq].remove_node_from_tail()
                del self.map_key_to_node[node_remove.key]
            self.min_freq = 1
            self.cache[self.min_freq].add_node_to_head(node)

        else:
            self._update_cache(key, val)

    def get(self, key: int) -> int:

        # edge case.
        if self.capacity == 0: return DUMMY_VALUE
        if key not in self.map_key_to_node: return DUMMY_VALUE

        # update the cache by accessing the key for 1+ time.
        node: DoubleListNode = self.map_key_to_node[key]
        self._update_cache(key, node.val)
        return node.val

    def _update_cache(self, key, val):
        """
        Update the key node.
        :param key:
        :return:
        """

        # update the val
        node: DoubleListNode = self.map_key_to_node[key]
        node.val = val

        # remove the old freq ll.
        self.cache[node.freq].remove_node(node)

        # update the min_frequency if the current key is the only min_freq node.
        if self.cache[node.freq].size == 0 and node.freq == self.min_freq:
            self.min_freq += 1

        # update the frequency cuz re-visited.
        node.freq += 1

        # add in the new freq ll.
        if node.freq not in self.cache:
            self.cache[node.freq] = DLL()
        self.cache[node.freq].add_node_to_head(node)


if __name__ == "__main__":
    lru_cache = LFUCache(3)
    lru_cache.put(1, 2)
    print(lru_cache)

    lru_cache.put(2, 3)
    print(lru_cache)

    lru_cache.put(3, 4)
    print(lru_cache)

    lru_cache.put(2, 5)
    print(lru_cache)

    lru_cache.put(1, 6)
    print(lru_cache)

    lru_cache.put(3, 3)
    print(lru_cache)

    lru_cache.get(2)
    print(lru_cache)

    lru_cache.put(10, 10)
    print(lru_cache)

    print(lru_cache.get(1))
