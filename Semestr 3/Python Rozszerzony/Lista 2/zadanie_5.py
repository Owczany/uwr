def kompresja(tekst):
    if not tekst:
        return []
    
    prev = tekst[0]
    count = 0
    res = []
    for letter in tekst:
        if prev == letter:
            count += 1
        else:
            res.append((count, prev))
            prev = letter
            count = 1
    res.append((count, prev))
    return res

def dekompresja(tekst_skompresowany):
    tekst = ''
    for times, letter in tekst_skompresowany:
        tekst += times * letter
    return tekst
    
tekst = 'sssuuuuper jesteś bracie!'

print(dekompresja(kompresja(tekst)))
print(kompresja(tekst))