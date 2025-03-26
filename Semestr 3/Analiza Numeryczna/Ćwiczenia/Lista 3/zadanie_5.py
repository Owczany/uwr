'''

Oznaczenia h zaburzenie w argumencie

nie chcemy brać czystych wartości jako wyznacznika uwarunkowania funkcji ponieważ nie będzie to obiektywna miara
zamiast tego chcemy policzyć o jaką część oryginalnego wyniku równi się wynik otrzymany

    Wskażnik funkcji:

    f(x+h) - f(x)
    -------------
        f(x)

checmey jednak uzależnić ten wskażnik o miarę zaburzenia ponieważ dla bardzo zaburzonych danych checmy mieć większy "margines błędu"

    wskaaźnik zaburzenia argumentu:

    h
    -           (odpowiada na pytanie jaką częścia x jest zaburzenie)
    x

wskaźnik umiarkowania definiowany jest jako stosunek względnej wartości funcji (wskaźnik funkcji) i względnej wartości argumentu (wskaźnik zaburzenia argumentu)


zaburzenie ma być małe więc zakładamy że dąży do zera.

Taylor dla f(x+h) = f(x) + f'(x) * h

    wskaźnik uwarunkowania:

    f(x+h) - f(x)
    -------------
        f(x)            (f(x+h) - f(x)) * x        podstawienie pod f(x+h) taylora       x*f'(x) * h        x* f'(x)
  ----------------- =   -------------------     ===================================    ---------------- = -----------
          h                   h * f(x)                                                      h*f(x)           f(x)
          -
          x



'''