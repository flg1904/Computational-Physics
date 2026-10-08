import numpy as np
import matplotlib.pyplot as plt
from Numeric_Integral import *

# region Aufgagabe 1a) 

"""
    Aufgabe 1a)

        Numerische Berechnung des Integrals

            ∫_0^1 1 / sqrt(1 - y^4) dy

        mit der Trapezregel, Simpsonregel und Gaußquadratur.
        Anschließend wird die Substitution

            y = sin(u)

        verwendet.
"""

# ------------------------------------------------------------
# Parameter und Integrationsgrenzen
# ------------------------------------------------------------

a = 4

y_anfang = 0
y_ende = 1

u_anfang = 0
u_ende = np.pi / 2

N_max = 10
N = np.arange(1, N_max + 1)

# ------------------------------------------------------------
# Integranden
# ------------------------------------------------------------

# Ursprüngliches Integral:
f_y = lambda y: 1 / np.sqrt(1 - y**a)

# Nach der Substitution y = sin(u):
f_u = lambda u: 1 / np.sqrt(1 + np.sin(u)**2)

# ------------------------------------------------------------
# Numerische Integration ohne Substitution
# ------------------------------------------------------------

trapez_ohne = []
simpson_ohne = []
gauss_ohne = []
exact_ohne = exact_integral(f_y, y_anfang, y_ende)

for n in N:
    trapez_ohne.append(Trapez_integral(n, f_y, y_anfang, y_ende))

    simpson_ohne.append(Simpson_integral(n, f_y, y_anfang, y_ende))

    gauss_ohne.append(Gaus_integral(n, f_y, y_anfang, y_ende))

# ------------------------------------------------------------
# Numerische Integration mit Substitution
# ------------------------------------------------------------

trapez_mit = []
simpson_mit = []
gauss_mit = []
exact_mit = exact_integral(f_u, u_anfang, u_ende)

for n in N:
    trapez_mit.append(Trapez_integral(n, f_u, u_anfang, u_ende))

    simpson_mit.append(Simpson_integral(n, f_u, u_anfang, u_ende))

    gauss_mit.append(Gaus_integral(n, f_u, u_anfang, u_ende))

# ------------------------------------------------------------
# Darstellung der Ergebnisse
# ------------------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Ohne Substitution ---------------------------------------

ax[0].plot(N, trapez_ohne, label="Trapezregel")
ax[0].plot(N, simpson_ohne, label="Simpsonregel")
ax[0].plot(N, gauss_ohne, label="Gaußregel")

ax[0].hlines(exact_ohne, 1, N_max, colors="k", linestyles="dashed", label="Exaktes Integral")

ax[0].set_xlabel("Anzahl der Intervalle")
ax[0].set_ylabel("Integralwert")
ax[0].set_title("Numerische Integration ohne Substitution")
ax[0].legend(loc="lower right")
ax[0].grid()


# --- Mit Substitution ----------------------------------------

ax[1].plot(N, trapez_mit, label="Trapezregel")
ax[1].plot(N, simpson_mit, label="Simpsonregel")
ax[1].plot(N, gauss_mit, label="Gaußregel")

ax[1].hlines(exact_mit, 1, N_max, colors="k", linestyles="dashed", label="Exaktes Integral")

ax[1].set_xlabel("Anzahl der Intervalle")
ax[1].set_ylabel("Integralwert")
ax[1].set_title("Numerische Integration mit Substitution")
ax[1].legend(loc="lower right")
ax[1].grid()

plt.tight_layout()
plt.show()

# endregion

# region Aufgabe 1b)

m = 1
n = 10

A = np.linspace(0.001, np.pi - 0.001, 100)

V_x = [
    lambda x: np.cosh(x),
    lambda x: np.exp(np.abs(x)),
    lambda x: -np.cos(x)
]

# Substitution: x = a * (1 - u^2)

x = lambda u, a: a * (1 - u**2)
dx = lambda u, a: 2 * a * u

u_anfang = 0
u_ende = 1

T_a_trapez_ges = []
T_a_simpson_ges = []
T_a_gauss_ges = []
T_a_soll_ges = []

for i, V in enumerate(V_x):

    T_a_trapez = []
    T_a_simpson = []
    T_a_gauss = []
    T_a_soll = []

    for a in A:

        if i == 0:
            grenzwert = 2 * np.sqrt(a / np.sinh(a))

        elif i == 1:
            grenzwert = 2 * np.sqrt(a / np.exp(a))

        else:
            grenzwert = 2 * np.sqrt(a / np.sin(a))

        def integrand(u):
            if u == 0:
                return grenzwert

            return dx(u, a) / np.sqrt(V(a) - V(x(u, a)))
        
        T_a_trapez.append(Trapez_integral(n, integrand, u_anfang, u_ende))
        T_a_simpson.append(Simpson_integral(n, integrand, u_anfang, u_ende))
        T_a_gauss.append(Gaus_integral(n, integrand, u_anfang, u_ende))
        T_a_soll.append(exact_integral(integrand, u_anfang, u_ende))

    T_a_trapez_ges.append(np.array(T_a_trapez))
    T_a_simpson_ges.append(np.array(T_a_simpson))
    T_a_gauss_ges.append(np.array(T_a_gauss))
    T_a_soll_ges.append(np.array(T_a_soll))


faktor = np.sqrt(8 * m)

titel = [
    r"$V(x) = \cosh(x)$",
    r"$V(x) = e^{|x|}$",
    r"$V(x) = -\cos(x)$"
]

fig, ax = plt.subplots(1, 3)
ax = ax.flatten()
for i in range(len(V_x)):

    ax[i].plot(A, T_a_trapez_ges[i] * faktor, label="Trapezregel")
    ax[i].plot(A, T_a_simpson_ges[i] * faktor, label="Simpsonregel")
    ax[i].plot(A, T_a_gauss_ges[i] * faktor, label="Gaußregel")
    ax[i].plot(A, T_a_soll_ges[i] * faktor, label="Exaktes Integral")
    ax[i].set_xlabel("a")
    ax[i].set_ylabel("T(a)")
    ax[i].set_title(titel[i])

    ax[i].legend()
    ax[i].grid()


plt.show()

# endregion


