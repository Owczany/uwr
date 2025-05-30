
def LCS(x: str, y: str, p: str = 'aaabb'):
    '''Longest Common Suffix'''
    n, m = len(x), len(y)

    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)] # Tworzymy 

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if x[i - 1] == y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])

    res = ''
    i, j = n, m
    while i > 0 and j > 0 and dp[i][j] != 0:
        if dp[i - 1][j - 1] != dp[i][j]:
            i, j = i - 1, j - 1
            res += x[i]
        elif dp[i - 1][j] < dp[i][j - 1]:
            j -= 1
            res += y[j]
        else:
            i -= 1
            x[i]
    return res[::-1]


# print(LCS('abc', 'bdakdac', ''))
