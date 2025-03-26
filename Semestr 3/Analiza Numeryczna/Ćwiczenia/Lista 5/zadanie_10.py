from math import log

e_ch = [
    0.763907023,
    0.543852762,
    0.196247370,
    0.009220859
]

e_a = [
    0.605426053,
    0.055322784,
    0.004819076,
    0.000399783
]

for p in range(1, 5):
    for i in range(len(e_ch) - 1):
        print(f'Porównanie błędu względnego ch{i + 1} z ch{i} dla p = {p}: {e_ch[i + 1] / (e_ch[i])**p}')
    print()
    
for p in range(1, 5):
    for i in range(len(e_a) - 1):
        print(f'Porównanie błędu względnego a{i + 1} z a{i} dla p = {p}: {e_a[i + 1] / (e_a[i])**p}')
    print()

for i in range(len(e_ch) - 2):
    print(f'p = {log(abs(e_ch[i + 2] / e_ch[i + 1])) / log(abs(e_ch[i + 1] / e_ch[i]))}')

print()

for i in range(len(e_a) - 2):
    print(f'p = {log(abs(e_a[i + 2] / e_a[i + 1])) / log(abs(e_a[i + 1] / e_a[i]))}')

# Dla chińczyków szybciej