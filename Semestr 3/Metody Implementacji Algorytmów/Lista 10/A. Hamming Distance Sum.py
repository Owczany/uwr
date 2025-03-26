a = input()
b = input()

def distance(s, t):
    d = 0
    for i in range(len(t) - len(s) + 1):
        for j in range(len(s)):
            if s[j] != t[j + i]:
                d += 1
    return d

print(distance(a, b))
