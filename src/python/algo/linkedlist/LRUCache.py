######################################################################################
#	Class: 					LRUCache
#	Author: 				Zhentao Xu (frankxu@umich.edu)
#	Date: 					2022/4/15
#	Description: 			Implement the LRU Cache.
#	Tested Environment:		Macbook pro w/ Python 3.9
######################################################################################

from typing import *

from src.python.algo.linkedlist.DoubleListNode import DoubleListNode

DUMMY_VALUE = -1


class LRUCache:

    def __init__(self, capacity: int = 100):
        self.capacity = capacity
        self.size = 0
        self.key_value_map: Dict[int, DoubleListNode] = dict()
        self.linked_list_dummy_head = DoubleListNode(0, 0, "DummyHead")
        self.linked_list_dummy_tail = DoubleListNode(0, 0, "DummyTail")
        self.linked_list_dummy_head.next, self.linked_list_dummy_tail.prev = self.linked_list_dummy_tail, self.linked_list_dummy_head

    def set(self, key: int, val: int):
        if key in self.key_value_map:
            node = self.key_value_map[key]
            node.val = val
            self.__remove_node(node)
            self.__insert_node_to_head(node)
        else:
            self.key_value_map[key] = DoubleListNode(key, val)
            node = self.key_value_map[key]
            self.__insert_node_to_head(node)
            self.size += 1
            if self.size > self.capacity:
                node = self.__remove_node_from_tail()
                self.size -= 1
                del self.key_value_map[node.key]

    def get(self, key: int) -> int:
        if key not in self.key_value_map:
            print("Error: key not found")
            return DUMMY_VALUE
        node = self.key_value_map[key]
        self.__remove_node(node)
        self.__insert_node_to_head(node)
        return node.val

    def __get_last_node(self) -> DoubleListNode:
        if self.size == 0:
            print("empty error")
            return None
        return self.linked_list_dummy_tail.prev

    def __insert_node_to_head(self, node: DoubleListNode) -> None:
        prev = self.linked_list_dummy_head
        next = prev.next
        prev.next, node.prev = node, prev
        node.next, next.prev = next, node
        if self.size > self.capacity:
            self.__remove_node_from_tail()

    def __remove_node_from_tail(self) -> DoubleListNode:
        if self.size == 0:
            print("size == 0, will not remove")
            return
        node = self.linked_list_dummy_tail.prev
        prev = self.linked_list_dummy_tail.prev.prev
        next = self.linked_list_dummy_tail
        prev.next, next.prev = next, prev
        return node

    def __remove_node(self, node):
        prev, next = node.prev, node.next
        prev.next, next.prev = next, prev

    def __str__(self):
        res = "==========" + "\n"
        res += "LRU: size = " + str(self.size) + "\n"
        res += "LRU: hash_dict = " + str({k: str(v.val) for k, v in self.key_value_map.items()}) + "\n"
        res += "LRU: linked_list = " + str(self.linked_list_dummy_head) + "\n"
        return res


if __name__ == "__main__":
    lru_cache = LRUCache(3)
    lru_cache.set(1, 2)
    print(lru_cache)

    lru_cache.set(2, 3)
    print(lru_cache)

    lru_cache.set(3, 4)
    print(lru_cache)

    lru_cache.set(4, 5)
    print(lru_cache)

    lru_cache.set(3, 3)
    print(lru_cache)

    lru_cache.set(3, 3)
    print(lru_cache)

    lru_cache.get(2)
    print(lru_cache)

    lru_cache.set(10, 10)
    print(lru_cache)

    print(lru_cache.get(1))
