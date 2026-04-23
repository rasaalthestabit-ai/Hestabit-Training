"""
Module for implementing the quick sort algorithm.

This module provides a function to sort lists of elements using the quick sort algorithm.
It uses a divide-and-conquer approach to achieve efficient sorting.

Author: [Your Name]
Date: [Today's Date]
"""

def quick_sort(arr: list) -> list:
    """
    Sorts a list of elements using the quick sort algorithm.

    Args:
        arr (list): The list of elements to be sorted.

    Returns:
        list: The sorted list of elements.

    Raises:
        TypeError: If the input is not a list.
        ValueError: If the list is empty.
    """
    # Check if input is a list
    if not isinstance(arr, list):
        raise TypeError("Input must be a list.")

    # Check if list is empty
    if len(arr) == 0:
        raise ValueError("List cannot be empty.")

    # Base case: If the list has one or zero elements, it is already sorted
    if len(arr) <= 1:
        return arr

    # Select the pivot element (in this case, the middle element)
    pivot = arr[len(arr) // 2]

    # Divide the list into three sub-lists: elements less than the pivot, equal to the pivot, and greater than the pivot
    left = [x for x in arr if x < pivot]  # Elements less than the pivot
    middle = [x for x in arr if x == pivot]  # Elements equal to the pivot
    right = [x for x in arr if x > pivot]  # Elements greater than the pivot

    # Recursively sort the sub-lists and combine the results
    return quick_sort(left) + middle + quick_sort(right)


if __name__ == "__main__":
    # Example usage:
    arr = [5, 2, 9, 1, 7, 3]
    print("Original list:", arr)
    sorted_arr = quick_sort(arr)
    print("Sorted list:", sorted_arr)