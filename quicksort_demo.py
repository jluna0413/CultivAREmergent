#!/usr/bin/env python3
"""
Quicksort Algorithm Implementation and Demo

This script demonstrates the quicksort algorithm with various examples.
"""

def quicksort(arr):
    """
    Sorts an array using the quicksort algorithm.

    Args:
        arr: List of comparable elements to sort

    Returns:
        Sorted list
    """
    if len(arr) <= 1:
        return arr

    # Choose pivot (using middle element for better performance)
    pivot_index = len(arr) // 2
    pivot = arr[pivot_index]

    # Partition the array into three parts
    left = []   # Elements less than pivot
    middle = [] # Elements equal to pivot
    right = []  # Elements greater than pivot

    for element in arr:
        if element < pivot:
            left.append(element)
        elif element == pivot:
            middle.append(element)
        else:
            right.append(element)

    # Recursively sort left and right partitions, then combine
    return quicksort(left) + middle + quicksort(right)


def main():
    """Demonstrate quicksort with various test cases."""

    print("=== Quicksort Algorithm Demo ===\n")

    # Test Case 1: Basic integers
    test1 = [3, 6, 8, 10, 1, 2, 1]
    print(f"Original: {test1}")
    sorted1 = quicksort(test1)
    print(f"Sorted:   {sorted1}\n")

    # Test Case 2: Already sorted
    test2 = [1, 2, 3, 4, 5]
    print(f"Already sorted: {test2}")
    sorted2 = quicksort(test2)
    print(f"Result:         {sorted2}\n")

    # Test Case 3: Reverse sorted
    test3 = [5, 4, 3, 2, 1]
    print(f"Reverse sorted: {test3}")
    sorted3 = quicksort(test3)
    print(f"Result:         {sorted3}\n")

    # Test Case 4: With duplicates
    test4 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    print(f"With duplicates: {test4}")
    sorted4 = quicksort(test4)
    print(f"Result:          {sorted4}\n")

    # Test Case 5: Single element
    test5 = [42]
    print(f"Single element: {test5}")
    sorted5 = quicksort(test5)
    print(f"Result:         {sorted5}\n")

    # Test Case 6: Empty list
    test6 = []
    print(f"Empty list: {test6}")
    sorted6 = quicksort(test6)
    print(f"Result:     {sorted6}\n")


if __name__ == "__main__":
    main()
