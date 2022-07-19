from typing import List


class QuickSort:

    @staticmethod
    def sort(arr):
        return QuickSort._sort(arr, 0, len(arr) - 1)

    @staticmethod
    def _sort(arr: List[int], l: int, r: int):
        """
        sort quick
        :param arr:
        :return:
        """
        if l > r: return
        if l == r: return
        p = QuickSort.partition(arr, l, r)
        QuickSort._sort(arr, l, p - 1)
        QuickSort._sort(arr, p + 1, r)
        return

    @staticmethod
    def partition(arr, l, r) -> int:
        """
        :param arr: input array
        :param l: left index. inclusive
        :param r: right index. inclusive
        :return: the partition index p, the arr[l, p] less than or equal to arr[p], arr[p, r] greater than or equal to arr[p]
        """
        if l > r: return None
        if l == r: return l
        pivot = arr[r]
        i = l - 1
        for j in range(l, r):
            if arr[j] <= pivot:
                arr[j], arr[i + 1] = arr[i + 1], arr[j]
                i += 1
        arr[r], arr[i + 1] = arr[i + 1], arr[r]
        return i + 1
