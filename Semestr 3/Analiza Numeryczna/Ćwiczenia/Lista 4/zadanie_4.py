import math

def fun(x):
    return x**2 -math.atan(x+2)

def bisekc(a1,b1,f):
    #krok pierwszy
    a = a1
    b = b1
    x0=0
    if(f(a) == 0):
        return a
    if(f(b) == 0):
        return b
    if(f(a)*f(b) > 0):
        print("blad")
        return

    e = abs(a-b)
    i = 0
    while(e>pow(10,-6)):
        i+=1
        x0 = (a+b)/2
        e/=2
        if(f(x0)==0):
            # print(f"x0 = {x0} f(x0) = {f(x0)}")
            return x0
        if(f(x0)*f(a) > 0):
            a = x0
        else:
            b = x0
        # print(f"n = {i+1} a = {a} b = {b} e = {e} f(a) = {f(a)} f(b) = {f(b)} ")
    print(f"n = {i + 1} a = {a} b = {b} e = {e} f(a) = {f(a)} f(b) = {f(b)} ")
    return x0

bisekc(-2, 0, fun)
bisekc(0, 2, fun)
