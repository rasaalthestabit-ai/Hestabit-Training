"""
Module for implementing the binary search algorithm.

This module provides a function to search for an element in a sorted list using the binary search algorithm.
The binary search algorithm is a fast search algorithm that finds the position of a target value within a sorted array.
It works by repeatedly dividing the list in half until the desired element is found.

Time Complexity: O(log n)
Space Complexity: O(1)
"""

def binary_search(sorted_list: list, target: int) -> int:
    """
    Searches for an element in a sorted list using the binary search algorithm.

    Args:
        sorted_list (list): A sorted list of integers.
        target (int): The target value to search for.

    Returns:
        int: The index of the target value if found, -1 otherwise.

    Raises:
        ValueError: If the input list is not sorted.
    """
    # Check if the input list is sorted
    if sorted_list != sorted(sorted_list):
        raise ValueError("Input list must be sorted")

    # Initialize the low and high pointers
    low = 0
    high = len(sorted_list) - 1

    # Continue searching until the low pointer is less than or equal to the high pointer
    while low <= high:
        # Calculate the mid index
        mid = (low + high) // 2  # Using integer division to avoid float results

        # If the target value is found at the mid index, return the mid index
        if sorted_list[mid] == target:
            return mid
        # If the target value is less than the value at the mid index, update the high pointer
        elif sorted_list[mid] > target:
            # Update the high pointer to mid - 1 to search in the left half
            high = mid - 1
        # If the target value is greater than the value at the mid index, update the low pointer
        else:
            # Update the low pointer to mid + 1 to search in the right half
            low = mid + 1

    # If the target value is not found, return -1
    return -1


if __name__ == "__main__":
    # Example usage:
    sorted_list = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    target = 23
    result = binary_search(sorted_list, target)
    print(f"Target {target} found at index {result}" if result != -1 else f"Target {target} not found in the list")