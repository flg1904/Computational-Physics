import numpy as np
import matplotlib.pyplot as plt
from Numeric_Integral import *
from Findig_zeros import *


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
N = np.arange(2, N_max + 1,2)

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

    gauss_ohne.append(Gaus_quadratur_integral(f_y, y_anfang, y_ende, n))

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

    gauss_mit.append(Gaus_quadratur_integral(f_u, u_anfang, u_ende, n))

# ------------------------------------------------------------
# Darstellung der Ergebnisse
# ------------------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12, 5), num = "Numerische Integration 1a)")
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
# plt.show()

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
        T_a_gauss.append(Gaus_quadratur_integral(lambda u: dx(u, a) / np.sqrt(V(a) - V(x(u, a))), u_anfang, u_ende, n))
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

# fig, ax = plt.subplots(2, 2)
# ax = ax.flatten()

# for i in range(len(V_x)):

#     ax[i].plot(A, T_a_trapez_ges[i] * faktor, label="Trapezregel")
#     ax[i].plot(A, T_a_simpson_ges[i] * faktor, label="Simpsonregel")
#     ax[i].plot(A, T_a_gauss_ges[i] * faktor, label="Gaußregel")
#     ax[i].plot(A, T_a_soll_ges[i] * faktor, label="Exaktes Integral")
#     ax[i].set_xlabel("a")
#     ax[i].set_ylabel("T(a)")
#     ax[i].set_title(titel[i])

#     ax[i].legend()
#     ax[i].grid()



fig, ax = plt.subplots(2, 2, num = "Abweichung der numerischen Integrale vom exakten Integral 1b)")
ax = ax.flatten()
for i in range(len(V_x)):

    ax[i].plot(A,np.abs(T_a_trapez_ges[i] * faktor - T_a_soll_ges[i] * faktor), label="Trapezregel")
    ax[i].plot(A, np.abs(T_a_simpson_ges[i] * faktor - T_a_soll_ges[i] * faktor), label="Simpsonregel")
    ax[i].plot(A, np.abs(T_a_gauss_ges[i] * faktor - T_a_soll_ges[i] * faktor), label="Gaußregel")
    ax[i].set_xlabel("a")
    ax[i].set_ylabel("T(a)")
    ax[i].set_title(titel[i])
    ax[i].set_yscale("log")
    ax[i].legend()
    ax[i].grid()


# plt.show()
# endregion

# region Aufgabe 2a)

# --------------------------------------------------
# 3. Parameter des Erde-Sonne-Systems
# --------------------------------------------------

M_sonne = 1.989e30
M_erde = 5.972e24
R = 1.496e11

mu = M_erde / (M_sonne + M_erde)

# --------------------------------------------------
# 4. Lagrange-Gleichung
# --------------------------------------------------

def f(x):
    return (x**5 + (mu - 3)*x**4 + (3 - 2*mu)*x**3 - mu*x**2 + 2*mu*x - mu)


def df(x):
    return (5*x**4 + 4*(mu - 3)*x**3 + 3*(3 - 2*mu)*x**2 - 2*mu*x + 2*mu)

# --------------------------------------------------
# 5. Nullstelle mit beiden Methoden berechnen
# --------------------------------------------------

# Für die definierte Variable x liegt L1 zwischen
# der Erde (x=0) und der Sonne (x=1).
# Die gesuchte Lösung liegt nahe bei x=1.

x_bis, Schritte_bis = Bisektionsverfahren(f, 0, 1)
x_newton, Schritte_newton = Newtonverfahren(f, df, 1)

print("Bisektionsverfahren:")
print("x =", x_bis)

print("\nNewton-Verfahren:")
print("x =", x_newton)

# --------------------------------------------------
# 6. Abstand von L1 zur Erde
# --------------------------------------------------

# Laut Aufgabenstellung gilt x = r/R,
# wobei r der Abstand von L1 zur Erde ist.
# Die Gleichung (9) verwendet jedoch x=r/R in
# Verbindung mit der ursprünglichen Gleichung.
#
# Für die vorliegende dimensionslose Gleichung
# liegt L1 bei x nahe 1.

r = x_newton * R

print("\nAbstand r = x * R:")
print(f"r = {r:.6e} m")
print(f"r = {r / 1000:.6e} km")

# --------------------------------------------------
# 7. Fehler für den Konvergenzvergleich
# --------------------------------------------------

# Eine hochgenaue Referenzlösung wird mit Newton
# und strenger Toleranz berechnet.

x_ref, _ = Newtonverfahren(f, df, 0.99, tol=1e-14)

fehler_bis = np.abs(Schritte_bis - x_ref)

fehler_newton = np.abs(Schritte_newton - x_ref)

# --------------------------------------------------
# 8. Diagramm: Konvergenzvergleich
# --------------------------------------------------

plt.figure(num="Konvergenzvergleich 2a)")

plt.semilogy(
    range(len(fehler_bis)),
    fehler_bis,
    "o-",
    label="Bisektionsverfahren"
)

plt.semilogy(
    range(len(fehler_newton)),
    fehler_newton,
    "o-",
    label="Newton-Verfahren"
)

plt.xticks(range(len(fehler_bis)))
plt.xlabel("Iteration n")
plt.ylabel("Fehler |x_n - x_ref|")
plt.title("Konvergenzvergleich")
plt.legend()
plt.grid(True)
# endregion

# region Aufgabe 2b)

# --------------------------------------------------
# 9. Quadratische Konvergenz des Newton-Verfahrens
# --------------------------------------------------

fehler = fehler_newton

# Fehler dürfen für die logarithmische Darstellung
# nicht null sein.

maske = ((fehler[:-1] > 0) & (fehler[1:] > 0))

e_n = fehler[:-1][maske]
e_n1 = fehler[1:][maske]

plt.figure(num="Quadratische Konvergenz des Newton-Verfahrens 2b)")

plt.loglog(e_n, e_n1, "o", label="Newton-Verfahren")

# Referenzkurve proportional zu e_n^2
if len(e_n) > 0:
    referenz = e_n**2
    plt.loglog(e_n, referenz, "--", label="Referenz: e_(n+1) ~ e_n^2")

plt.xlabel("Fehler e_n")
plt.ylabel("Fehler e_(n+1)")
plt.title("Überprüfung der quadratischen Konvergenz")
plt.legend()
plt.grid(True)

# plt.show()
#endregion

# region Aufgabe 3a)

nullstellen_pression = 1e-4
versuche = 20

anz_nullstellen = []

pr = False

for _ in range(versuche):
    a = np.random.uniform(0, 1, 7)

    f = np.poly1d(a)
    df = np.polyder(f)

    x_werte = np.linspace(-10, 10, 10001)

    nullstellen = []

    for i in range(len(x_werte) - 1):
        a = x_werte[i]
        b = x_werte[i + 1]

        if f(a) * f(b) < 0:
            nullstelle, schritte = Bisektionsverfahren(f, a, b)
            nullstellen.append(nullstelle)

    if len(nullstellen) == 0:
        anz_nullstellen.append(0)
        continue
    else:
        nullstellen.sort()
        eindeutige_nullstellen = [nullstellen[0]]

        for x in nullstellen[1:]:
            if abs(x - eindeutige_nullstellen[-1]) > nullstellen_pression:
                eindeutige_nullstellen.append(x)

        if pr == False:
            plt.figure(num = "Verteilung der reellen Nullstellen 3a)")
            plt.plot(x_werte, f(x_werte), label="Polynom")
            plt.plot(eindeutige_nullstellen, f(eindeutige_nullstellen), "ro", label="Nullstellen")
            plt.hlines(0, -10, 10, "k", label="x-Achse")
            # plt.vlines(durchschnitt, ymin=0, ymax=5, colors="r", linestyles="dashed", label="Durchschnitt")
            plt.xlabel("Nullstelle x")
            plt.ylabel("Häufigkeit")
            plt.title("Verteilung der reellen Nullstellen")
            pr = True
        anz_nullstellen.append(len(eindeutige_nullstellen))


print(f"Durchschnittliche Anzahl der reellen Nullstellen: {np.mean(anz_nullstellen):.2f}")

plt.show()



# endregion