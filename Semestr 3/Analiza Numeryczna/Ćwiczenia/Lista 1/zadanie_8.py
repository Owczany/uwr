import math

'''
Mamy funkcję log2(x), która dla argumentu x ∈ [1, 2] ma dokładny wynik
Do rozwiązania potrzebowaliśmy podstawowej właśności logarytmów
log a (x) + log a (y) = log a (x * y)
log a (x) - log a (y) = log a (x / y)


Dla x ∈ (2, 1024]
def log2_1(x):
    res = 0
    while x > 2:
        x = x / 2
        res += log2(2)
    res += log2(x)
    return res

Dla x ∈ [1/1024; 1)
def log2_2(x):
    res = 0
    while x < 1:
        x = x * 2
        res -= log2(2)
    res += log2(x)
    return res
'''

def log2_1(x):
    res = 0
    while x > 2:
        x = x / 2
        res += math.log2(2) # 1 
    res += math.log2(x)
    return res

def log2_2(x):
    res = 0
    while x < 1:
        x = x * 2
        res -= math.log2(2) # 1
    res += math.log2(x)
    return res

print(f"Moja funkcja {log2_1(10)}, kontrolna funkcja: {math.log2(10)}")
print(f"Moja funkcja {log2_2(1/100)}, kontrolna funkcja: {math.log2(1/100)}")
