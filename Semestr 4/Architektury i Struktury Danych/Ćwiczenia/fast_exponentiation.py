def pow_rec(x, n):
    # Jeśli podstawa wynosi zero to jego potęga to 0
    if x == 0:
        return 0
    
    # Natomiast jeśli x jest różny od zera i n jest równe 0 to zwróć 1 
    if n == 0:
        return 1 
    
    result = pow(x, n // 2)
    
    if n % 2 == 1:
        return x * result * result
    else:
        return result * result

def pow_iter(x, n):
    # Jeśli podstawa wynosi zero to jego potęga to 0
    if x == 0:
        return 0
    
    # Natomiast jeśli x jest różny od zera i n jest równe 0 to zwróć 1 
    if n == 0:
        return 1 
    
    w = x
    n = n // 2
    while n > 0:
        if n % 2 == 1:
            w = x * w * w
        else:
            w = w * w
        
        n = n // 2
    return w

print(pow_rec(2, 8))
print(pow_iter(2, 8))

# Czaję bazke O(log(n)) oraz O(log(n) * log(x) * log(x))