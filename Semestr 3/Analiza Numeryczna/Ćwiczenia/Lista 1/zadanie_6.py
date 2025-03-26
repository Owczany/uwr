import math

# k = 2000000, żeby było z błędem mniejszym niż 10^-6
krok = 4
pi = 0
k = 0

while abs(krok) > 10 ** -6:
    k += 1
    pi += krok
    krok = (4 * (-1) ** k) / (2*k + 1)
    print(pi)
    
print(k)

# wyniki się zgadzają z rzeczywistością