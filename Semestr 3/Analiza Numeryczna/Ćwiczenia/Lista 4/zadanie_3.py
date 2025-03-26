def f(x):
    return x - 0.49

a0 = 0.0
b0 = 1.0
en = []

def bisekcja(f, a, b):
    for _ in range(5):
        mid = (a + b) / 2
        en.append(abs(mid - 0.49))
        if f(mid) == 0:
            return mid
        
        if f(mid) < 0:
            a = mid
        else:
            b = mid
    return (a + b) / 2

print(bisekcja(f, a0, b0))
for ans in en:
    print(ans)
