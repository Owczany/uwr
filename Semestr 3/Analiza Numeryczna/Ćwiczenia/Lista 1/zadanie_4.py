# Napisane w podwójnej precyzji
def ciag(n):
    yn = [1, -(1/6)]
    if n == 0:
        return yn[0]
    
    if n == 1:
        return yn[1]
    
    for i in range(2, n + 1):
        yn.append((35/6)*yn[i-1] + yn[i-2])
        print(f"n = {i}")
        print(yn[-1])
        print('-' * 50)

print(ciag(50))
    
# Rozwiązanie
'''
y0 = 1
y1 = -1/6
y2 = 1/36
y3 = -1/216

łatwo zauważyć, że jawny wzór na ten ciąg to yn = (-1)^n / 6^n
z tego wynika, że jest on malejący i z dalszym n-em numery tego
ciągu powinny się zbliżać do 0
'''
