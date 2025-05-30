nums: list[int] = [3, 2, 2]

def sum_3(nums: list[int], target: int):
    nums.sort() # Quick Sort / Merge Sort nlog(n)
    
    # Teraz po n elementach robimy TWO SUM
    for i in range(len(nums) - 2):
        l, r = i + 1, len(nums) - 1
        while l < r:
            sum = nums[i] + nums[l] + nums[r]
            # Wynik jeśli jest git
            if sum == target:
                return True
            elif sum < target:
                l += 1
            else:
                r -= 1
    
    return False

print(sum_3(nums, 7))
