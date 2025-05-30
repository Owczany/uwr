# TODO: Przekminić

# Zakładamy, ze liczby są z przedziału <0, k>
def counting_sort(A, k):
    
    B = [0 for _ in range(len(A))]

    # Inicjalizacja zliczania
    c = [0 for _ in range(0, k + 1)]

    # Drugi krok to zliczenie tych liczb ile razy wystepuja
    for num in A:
        c[num] += 1

    # wiemy, ze liczby wieksze 
    for i in range(1, k + 1):
        c[i] += c[i - 1]
    
    # Tworzenie odpowiedzi
    for i in range(len(A) - 1, -1 ,-1):
        B[c[A[i]] - 1] = A[i]
        c[A[i]] -= 1

    return B



print(counting_sort([4, 2, 10], 10))