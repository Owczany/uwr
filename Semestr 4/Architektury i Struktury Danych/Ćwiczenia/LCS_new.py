X = 'axxxaaa'
Y = 'axxx'

def LCS(x: str, y: str, p: str = 'aaabb'):
    n, m, k = len(x), len(y), len(p)

    dp = [[[0 for _ in range(m + 1)] for _ in range(n + 1)] for _ in range(k + 1)] # Tworzymy 

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1] == p[0]:
                dp[1][i][j] = dp[0][i - 1][j - 1] + 1
                dp[0][i][j] = max(dp[0][i - 1][j], dp[0][i][j - 1])
            elif x[i - 1] == y[j - 1]:
                dp[0][i][j] = dp[0][i - 1][j - 1] + 1
            else:
                dp[0][i][j] = max(dp[0][i][j - 1], dp[0][i - 1][j])

    for s in range(1, k + 1):
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # if dp[s][i][j]:
                #     continue

                if x[i - 1] == y[j - 1] and p[s - 1] and s < k:
                    dp[s + 1][i][j] = max(dp[s + 1][i][j], dp[s][i - 1][j - 1] + 1)
                elif x[i - 1] == y[j - 1]:
                    dp[s][i][j] = max(dp[s][i - 1][j - 1] + 1, dp[s][i][j], dp[s][i - 1][j], dp[s][i][j - 1])
                
                dp[s][i][j] = max(dp[s][i - 1][j], dp[s][i][j - 1])

    return dp

print(LCS(X, Y)[1])


