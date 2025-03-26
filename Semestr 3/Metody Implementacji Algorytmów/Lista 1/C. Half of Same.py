from collections import Counter

n = int(input())
nums = list(map(int, input().split()))
counter = Counter(nums)
k = 1
for key in counter:
    k = max(k, key)
    if counter[key] >= n // 2:
        print('-1')
        break

def find_max_k(counter,i):
    for k in range(i, 0, -1):
        rest_counter = Counter()
        for key in counter:
            rest_counter[key % k] += counter[key]
            if rest_counter[key] >= n // 2:
                print(k)
                return
    
find_max_k(counter, k)