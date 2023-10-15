"""
An utility helpers module
"""


def last_index_of_element(arr, element):
    for i in range(len(arr) - 1, -1, -1):
        if arr[i] == element:
            return i
    return -1
