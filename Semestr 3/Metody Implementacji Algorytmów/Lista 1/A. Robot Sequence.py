n = int(input())
comands = input()

def routes(n, comands):
    res = 0
    for left in range(n):
        vertical = 0
        horizontal = 0
        for right in range(left, n):

            match comands[right]:
                case "U":
                    vertical += 1
                case "D":
                    vertical -= 1
                case "R":
                    horizontal += 1
                case "L":
                    horizontal -= 1

            if not vertical and not horizontal:
                res += 1
    return res

print(routes(n, comands))
