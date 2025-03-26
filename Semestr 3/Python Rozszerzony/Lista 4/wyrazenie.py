from abc import ABC, abstractmethod

# Wyjątki
class VariableNotFoundException(Exception):
    pass

class InvalidExpressionException(Exception):
    pass

# Klasa bazowa Wyrazenie
class Wyrazenie(ABC):
    @abstractmethod
    def oblicz(self, zmienne):
        pass
    
    @abstractmethod
    def uprosc(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

    def __add__(self, other):
        if isinstance(other, Wyrazenie):
            return Dodaj(self, other)
        else:
            raise InvalidExpressionException("Można dodawać tylko obiekty typu Wyrazenie")
    
    def __mul__(self, other):
        if isinstance(other, Wyrazenie):
            return Razy(self, other)
        else:
            raise InvalidExpressionException("Można mnożyć tylko obiekty typu Wyrazenie")

# Klasa Stala
class Stala(Wyrazenie):
    def __init__(self, wartosc):
        self.wartosc = wartosc
    
    def oblicz(self, zmienne):
        return self.wartosc
    
    def uprosc(self):
        return self
    
    def __str__(self):
        return str(self.wartosc)

# Klasa Zmienna
class Zmienna(Wyrazenie):
    def __init__(self, nazwa):
        self.nazwa = nazwa
    
    def oblicz(self, zmienne):
        if self.nazwa in zmienne:
            return zmienne[self.nazwa]
        else:
            raise VariableNotFoundException(f"Zmienna '{self.nazwa}' nie została znaleziona")
        
    def uprosc(self):
        return self
    
    def __str__(self):
        return self.nazwa

# Klasa Dodaj
class Dodaj(Wyrazenie):
    def __init__(self, lewy, prawy):
        self.lewy = lewy
        self.prawy = prawy
    
    def oblicz(self, zmienne):
        return self.lewy.oblicz(zmienne) + self.prawy.oblicz(zmienne)
    
    def uprosc(self):
        lewa = self.lewy.uprosc()
        prawa = self.prawy.uprosc()
        if isinstance(lewa, Stala) and isinstance(prawa, Stala):
            return Stala(lewa.wartosc + prawa.wartosc)
        return Dodaj(lewa, prawa)
    
    def __str__(self):
        return f"({self.lewy} + {self.prawy})"

# Klasa Razy
class Razy(Wyrazenie):
    def __init__(self, lewy, prawy):
        self.lewy = lewy
        self.prawy = prawy
    
    def oblicz(self, zmienne):
        return self.lewy.oblicz(zmienne) * self.prawy.oblicz(zmienne)
    
    def uprosc(self):
        lewa = self.lewy.uprosc()
        prawa = self.prawy.uprosc()
        if isinstance(lewa, Stala) and isinstance(prawa, Stala):
            if lewa.wartosc == 0 or prawa.wartosc == 0:
                return Stala(0)
            return Stala(lewa.wartosc * prawa.wartosc)
        return Razy(lewa, prawa)
    
    def __str__(self):
        return f"({self.lewy} * {self.prawy})"

# Przykład użycia
if __name__ == "__main__":
    wyrazenie = Razy(Dodaj(Zmienna("x"), Stala(2)), Zmienna("y"))
    print(wyrazenie)  # Wyświetla: ((x + 2) * y)
    wyrazenie2 = Dodaj(Stala(4), Razy(Zmienna('x'), Dodaj(Stala(2), Stala(-2)))) 
    print(wyrazenie2)
    try:
        wynik = wyrazenie.oblicz({"x": 3, "y": 4})
        print("Wynik:", wynik)  # Wyświetla: Wynik: 20

        print(wyrazenie2.uprosc())

    except VariableNotFoundException as e:
        print(e)
    except InvalidExpressionException as e:
        print(e)
