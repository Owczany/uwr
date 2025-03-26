n = int(input())

for _ in range(n):
    t = int(input())

    if t // 2 % 2 == 1:
        print('NO')
    else:
        print('YES')
        num = 2
        for _ in range(t // 2):
            print(num, end=' ')
            num += 2

        num = 1
        for _ in range(t // 2 - 1):
            print(num, end=' ')
            num += 2
        
        print(num + (t // 2))
