from collections import Counter

lista_slow = ["Cyprian", "cyberotoman", "cynik", "ceniąc", "czule"]
lista_slow_test = ["Para", "PaPa", "Patson", "rodak", "rodzaj", "rokit", "rostac", "rower"]

def common_prefix(lista_slow):
    prefix_counter = Counter()
    res = ""
    count = 0

    # Zliczamy wszyskie mozliwe prefixy
    for word in lista_slow:
        for i in range(len(word)):
            prefix_counter[word[:i+1].lower()] += 1

    # Sprawdzamy, który jest najdłuzszy i najczesciej wystepuje
    for key in prefix_counter.keys():
        if prefix_counter[key] >= 3:
            if (len(key) > len(res)) or (len(key) == len(res) and count < prefix_counter[key]):
                res = key
                count = prefix_counter[key]

    return res

print(common_prefix(lista_slow))
print(common_prefix(lista_slow_test))
