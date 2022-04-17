from src.python.algo.linkedlist.LRUCache import LRUCache


def test_lru_cache():
    lru_cache = LRUCache(3)
    lru_cache.set(1, 2)
    assert (lru_cache.get(1) == 2)

    lru_cache.set(2, 3)
    print(lru_cache)

    lru_cache.set(3, 4)
    print(lru_cache)

    lru_cache.set(4, 5)
    print(lru_cache)

    assert (lru_cache.get(1) == -1)
    assert (lru_cache.get(2) == 3)

    lru_cache.set(10, 10)
    print(lru_cache)

    assert (lru_cache.get(3) == -1)


if __name__ == "__main__":
    res = test_lru_cache()
