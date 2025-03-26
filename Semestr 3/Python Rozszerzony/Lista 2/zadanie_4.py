import random

# Tekst to be or not to be
f = open('to_be_or_not_to_be.txt', 'r+')

def uprosc_zdanie(tekst, dl_slowa, liczba_slow):
    words = []
    
    # Usuwamy za długie słowa
    for word in tekst.replace('.', '').replace(',', '').split():
        if len(word) <= dl_slowa:
            words.append(word)
    
    # Usuwamy za dużą ilość słów
    while len(words) > liczba_slow:
        del words[random.randint(0, len(words) - 1)]
    
    # Upewniamy się, że pierwsza litera jest duża i na końcu jest kropka
    if not words:
       return '' 
    res = words[0][0].upper() + words[0][1:] + ' '
    res += (' ').join(words[1:]) + '.'
    return res
    
    
tekst = "Podział peryklinalny inicjałów wrzecionowatych \
kambium charakteryzuje się ścianą podziałową inicjowaną \
w płaszczyźnie maksymalnej."

print(uprosc_zdanie(tekst, 10, 5))

# https://www.poetryfoundation.org/poems/56965/speech-to-be-or-not-to-be-that-is-the-question
tekst_literatura = f.readlines()

for tekst in tekst_literatura:
    # print(tekst)
    print(uprosc_zdanie(tekst, 5, 2))

