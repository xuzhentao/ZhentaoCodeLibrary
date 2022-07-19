from src.python.algo.sort.QuickSort import QuickSort


def test_partition():
    data = [1, 5, 3, 4, 7, 6, 4, 5, 8, 7, 5]
    res = QuickSort.partition(data, 0, len(data) - 1)
    assert (res == 6)


def test_sort():
    data = [1, 5, 3, 4, 7, 6, 4, 5, 8, 7, 5]
    data_cp = data[:]
    QuickSort.sort(data_cp)
    assert (data_cp == sorted(data))


if __name__ == "__main__":
    test_partition()
    test_sort()
