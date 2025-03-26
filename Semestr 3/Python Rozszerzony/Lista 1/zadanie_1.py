from decimal import Decimal

# Bez biblioteki Decimal
def vat_faktura(prices):
    total = 0
    for price in prices:
        total += price
    return total * 0.23

def vat_paragon(prices):
    total = 0
    for price in prices:
        total += price * 0.23
    return total

# Z biblioteka Decimal
def vat_fakturaD(prices):
    total = Decimal(0)  
    for price in prices:
        total += Decimal(price)  
    # print(total * Decimal(0.23))
    return total * Decimal(0.23) 

def vat_paragonD(prices):
    total = Decimal(0)  
    for price in prices:
        total += Decimal(price) * Decimal(0.23)  
    # print(total)
    return total

prices1 = [1.01, 2.13, 25.23, 1999.99] # ostatnie zamień na 1999.99
prices2 = [199.99, 2000.00, 0.1, 0.2]
prices3 = [0.2, 0.7]

# Sprawdzanie wyników
print(vat_faktura(prices1) == vat_paragon(prices1))     # True
print(vat_faktura(prices2) == vat_paragon(prices2))     # False
print(vat_faktura(prices3) == vat_paragon(prices3))     # False

print(vat_fakturaD(prices1) == vat_paragonD(prices1))   # True / False dziwne xD
print(vat_fakturaD(prices2) == vat_paragonD(prices2))   # True
print(vat_fakturaD(prices3) == vat_paragonD(prices3))   # True
