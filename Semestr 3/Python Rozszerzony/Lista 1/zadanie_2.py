
# Funckja sprawdzająca czy tekst jest palindromem
def is_palindrom(s):
    s = s.lower()
    l, r = 0, len(s) - 1
    while l < r:
        while not s[l].isalnum():
            l += 1
        
        while not s[r].isalnum():
            r -= 1

        if s[l] != s[r]:
            return False
        
        l += 1
        r -= 1

    return True

print(is_palindrom('Ala ma kota a kot ma ale!'))            # False
print(is_palindrom("Eine güldne, gute Tugend: Lüge nie!"))  # True
print(is_palindrom("Míč omočím."))                          # True
