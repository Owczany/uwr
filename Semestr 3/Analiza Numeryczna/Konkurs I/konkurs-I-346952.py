# Importowanie modułów potrzbnych do zadania
import numpy as np
import matplotlib.pyplot as plt

def interpolacja_wspolczynniki(t, y):
    n = len(t) - 1  # liczba przedziałów
    h = np.diff(t)  # długość przedziałów
    b_diff = np.diff(y) / h

    A = np.zeros((n + 1, n + 1)) #macierz układu równań dla drugich pochodnych
    rhs = np.zeros(n + 1)  # prawa strona równania


    A[0, 0] = 1
    A[n, n] = 1

    # drugie pochodne
    for i in range(1, n):
        A[i, i - 1] = h[i - 1]
        A[i, i] = 2 * (h[i - 1] + h[i])
        A[i, i + 1] = h[i]
        rhs[i] = 6 * (b_diff[i] - b_diff[i - 1])

    # rozwiązanie układu równań
    M = np.linalg.solve(A, rhs)


    coefs = []
    for i in range(n): #wyliczenie współczynników
        a_coef = y[i]
        b_coef = b_diff[i] - h[i] * (2 * M[i] + M[i + 1]) / 6
        c_coef = M[i] / 2
        d_coef = (M[i + 1] - M[i]) / (6 * h[i])
        coefs.append((a_coef, b_coef, c_coef, d_coef, t[i]))

    return coefs


def wylicz_z_wspolczynniki(coefs, x):
    y = np.zeros_like(x)
    for a, b, c, d, t0 in coefs:
        mask = (x >= t0) #true gdzie skleja false gdzie nie
        if mask.any():
            dx = x[mask] - t0
            y[mask] = a + b * dx + c * dx**2 + d * dx**3
    return y


# Dane wejściowe
# x = np.array([15.5, 12.5, 8, 10, 7, 4, 8, 10, 9.5, 14, 18, 17, 22, 25, 19,
#               24.5, 23, 17, 16, 12.5, 16.5, 21, 17, 11, 5.5, 7.5, 10, 12])
# y = np.array([32.5, 28.5, 29, 33, 33, 37, 39.5, 38.5, 42, 43.5, 42, 40, 41.5, 37, 35,
#               33.5, 29.5, 30.5, 32, 19.5, 24.5, 22, 15, 10.5, 2.5, 8, 14.5, 20])

def plotuj(list_x, list_y):
    plt.figure(figsize=(10, 6))
    for x1, y1 in zip(list_x, list_y):
        x = np.array(x1)
        y = np.array(y1)
        t = np.linspace(0, 1, len(x))  # Węzły
        coefs_x = interpolacja_wspolczynniki(t, x)
        coefs_y = interpolacja_wspolczynniki(t, y)

        M = 1000000
        u = np.linspace(0, 1, M)
        sx_u = wylicz_z_wspolczynniki(coefs_x, u)
        sy_u = wylicz_z_wspolczynniki(coefs_y, u)
        plt.plot(sx_u, sy_u, '-', label='Łamana interpolacyjna')
    plt.axis('equal')
    plt.show()

x =[
    [47, 48, 48, 49, 49, 49, 49, 49, 50, 50, 47, 46, 44, 44, 45, 49, 54, 61, 67, 75, 81, 80, 76, 71, 66, 59, 52],
[104,  105, 105, 105, 105, 104, 104, 104, 104, 104, 104, 103, 103, 103, 102, 102, 102, 103, 103, 104, 105, 107, 109, 111, 111, 112, 113, 113, 114, 114, 116, 117, 118, 120, 121, 122, 124, 126, 129, 131, 133, 136, 138, 141, 143, 146, 146, 148, 148, 149, 149, 149, 149, 148, 148, 147, 146, 146, 145, 145],

    ]
y = [
    [64, 72, 79, 85, 94, 104, 112, 120, 129, 136, 126, 115, 102, 88, 78, 70, 67, 64, 62, 63, 70, 79, 88, 94, 99, 103, 105],
[67,  70, 74, 77, 79, 82, 84, 87, 90, 93, 95, 100, 102, 106, 110, 112, 115, 117, 120, 121, 123, 123, 120, 115, 111, 108, 105, 101, 97, 95, 95, 97, 99, 101, 104, 106, 109, 111, 114, 117, 119, 122, 123, 123, 122, 117, 114, 111, 107, 103, 100, 96, 93, 90, 87, 83, 80, 78, 75, 73],

]

plotuj(x,y)
# x = np.array([47, 48, 48, 49, 49, 49, 49, 49, 50, 50, 47, 46, 44, 44, 45, 49, 54, 61, 67, 75, 81, 80, 76, 71, 66, 59, 52])
# y = np.array([64, 72, 79, 85, 94, 104, 112, 120, 129, 136, 126, 115, 102, 88, 78, 70, 67, 64, 62, 63, 70, 79, 88, 94, 99, 103, 105])
# t = np.linspace(0, 1, len(x))  # Węzły
# coefs_x = interpolacja_wspolczynniki(t, x)
# coefs_y = interpolacja_wspolczynniki(t, y)
#
# M = 1000
# u = np.linspace(0, 1, M)
# sx_u = wylicz_z_wspolczynniki(coefs_x, u)
# sy_u = wylicz_z_wspolczynniki(coefs_y, u)
#
# # Rysowanie wynikowej łamanej
# plt.figure(figsize=(10, 6))
# # plt.plot(x, y, 'o', label='Punkty (xk, yk)')
# plt.plot(sx_u, sy_u, '-', label='Łamana interpolacyjna')
# plt.title("Interpolacja funkcją sklejaną 3 stopnia")
# # plt.xlabel("x")
# # plt.ylabel("y")
# # plt.legend()
# # plt.grid()
# plt.axis('equal')
# plt.show()
#
# # x = np.array([47, 48, 48, 49, 49, 49, 49, 49, 50, 50, 47, 46, 44, 44, 45, 49, 54, 61, 67, 75, 81, 80, 76, 71, 66, 59, 52])
# # y = np.array([64, 72, 79, 85, 94, 104, 112, 120, 129, 136, 126, 115, 102, 88, 78, 70, 67, 64, 62, 63, 70, 79, 88, 94, 99, 103, 105])
# # t = np.linspace(0, 1, len(x))  # Węzły
# #
# # coefs_x = interpolacja_wspolczynniki(t, x)
# # coefs_y = interpolacja_wspolczynniki(t, y)
# #
# #
# # M = 1000
# # u = np.linspace(0, 1, M)
# # sx_u = wylicz_z_wspolczynniki(coefs_x, u)
# # sy_u = wylicz_z_wspolczynniki(coefs_y, u)
# #
# # # Rysowanie wynikowej łamanej
# # plt.figure(figsize=(10, 6))
# # # plt.plot(x, y, 'o', label='Punkty (xk, yk)')
# # plt.plot(sx_u, sy_u, '-', label='Łamana interpolacyjna')
# # plt.xlabel("x")
# # plt.ylabel("y")
# # plt.legend()
# # plt.grid()
# # plt.axis('equal')
# # plt.show()
# #
#
