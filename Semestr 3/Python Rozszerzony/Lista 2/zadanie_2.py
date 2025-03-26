# Funkcja sudan, bez memoizacji
def sudan(n, x, y):
    # Warunek bazowy
    if n == 0:
        return x + y
    
    if y == 0:
        return x

    return sudan(n - 1, sudan(n, x, y - 1), sudan(n, x, y - 1) +  y + 1)

# Funkcja sudan z memoizacją
def sudan_memo(n, x, y):
    # Nasza pamięć
    memo = {}
    
    def sudan(n, x, y):
        # Jeśli wyliczyliśmy już wcześniej odpowiedź to ją zwróć
        if (n, x, y) in memo:
            return memo[(n, x, y)]
        
        # Jeśli nie znamy to wylicz
        if n == 0:
            result = x + y
        elif y == 0:
            result = x
        else:
            result = sudan(n - 1, sudan(n, x, y - 1), sudan(n, x, y - 1) +  y + 1)
        
        # Zapisz w pamięci
        memo[(n, x, y)] = result
        return result
    
    return sudan(n, x, y)

print(sudan_memo(2, 2, 2))
print(sudan(2, 1, 2))
    