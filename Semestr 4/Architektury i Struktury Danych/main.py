x = 'bb'
y =  'bb'
print(x.count('b'))
print(x.count('a'))
p = 'aaabb'

n = len(x)
m = len(y)
print(n)
print(m)
len_p = len(p)

# Inicjalizacja dp
dp = [[[0] * (len_p + 1) for _ in range(m + 1)] for _ in range(n + 1)]
dp[0][0][0] = 0  # startujemy bez niczego dopasowanego


for k in range(0, len_p + 1):
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                if k < len_p and x[i - 1] == p[k]:
                    dp[i][j][k + 1] = max(dp[i][j][k + 1], dp[i - 1][j - 1][k] + 1)

                else:
                    dp[i][j][k] = max(dp[i][j][k], dp[i - 1][j - 1][k] + 1)

            dp[i][j][k] = max(dp[i][j][k], dp[i][j - 1][k], dp[i - 1][j][k])

# for k in range(0, len_p + 1):
#     for i in range(1, n + 1):
#         for j in range(1, m + 1):
#             if x[i - 1] == y[j - 1]:
#                 if k < len_p and x[i - 1] == p[k]:
#                     dp[i][j][k + 1] = max(dp[i][j][k + 1], dp[i - 1][j - 1][k] + 1)

#                 else:
#                     dp[i][j][0] = max(dp[i][j][0], dp[i - 1][j - 1][k] + 1)

#             dp[i][j][k] = max(dp[i][j][k], dp[i][j - 1][k], dp[i - 1][j][k])


