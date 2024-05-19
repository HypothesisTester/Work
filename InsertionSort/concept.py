def insertionSort(arr):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        j = i - 1
        while j >= 0 and arr[j + 1 < arr[j]]:
            # arr[j] and arr[j + 1] are out of order so swap them 