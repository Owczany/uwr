# Greedy-Iterative-Activity-Selector(A, s, f): 

#     Sort A by finish times stored in f
#     S = {A[1]} 
#     k = 1
    
#     n = A.length
    
#     for i = 2 to n:
#         if s[i] ≥ f[k]: 
#             S = S U {A[i]}
#             k = i
    
#     return S

I = [(-10, 10), (2, 4), (2, 3) , (4, 6)]

def sort(A):
    for i in range(len(A)):
        for j in range(i + 1, len(A)):
            if A[j][1] < A[i][1]:
                A[i], A[j] = A[j], A[i]
    return A

print(sort(I))

def greedy_iterative_activity_selector(A):
    A = sort(A)
    S = {A[0]}
    f = A[0][1]
    

    for i in range(1, len(A)):
        if A[i][0] > f:
            f = A[i][1]
            S.add(A[i])
        
    return S

print(greedy_iterative_activity_selector(I))