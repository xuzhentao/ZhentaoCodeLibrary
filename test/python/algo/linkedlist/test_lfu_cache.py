from src.python.algo.linkedlist.LFUCache import LFUCache


def test_lfu_cache():
    lfu_cache = LFUCache(3)
    lfu_cache.put(1, 2)
    print(lfu_cache)
    assert (lfu_cache.min_freq == 1)
    assert (lfu_cache.size == 1)

    lfu_cache.put(2, 3)
    print(lfu_cache)
    assert (lfu_cache.min_freq == 1)
    assert (lfu_cache.size == 2)

    lfu_cache.put(3, 4)
    print(lfu_cache)
    assert (lfu_cache.min_freq == 1)
    assert (lfu_cache.size == 3)

    lfu_cache.put(2, 5)
    print(lfu_cache)

    lfu_cache.put(1, 6)
    print(lfu_cache)

    lfu_cache.put(3, 3)
    print(lfu_cache)

    assert (lfu_cache.min_freq == 2)

    assert (lfu_cache.get(2) == 5)


if __name__ == "__main__":
    test_lfu_cache()
