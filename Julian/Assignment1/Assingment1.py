import numpy as np
import matplotlib.pyplot as plt
from Numeric_Integral import *
from Findig_zeros import *


# region Aufgagabe 1a) 

# Berechnet F = ∫_0^1 dy / sqrt(1 - y^4) mit Trapez-, Simpson- und Gaußregel,
# jeweils ohne und mit Substitution y = sin(u), und vergleicht die Konvergenz.

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

y_start = 0
y_end = 1

u_start = 0
u_end = np.pi / 2

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

trapezoid_no_sub = []
simpson_no_sub = []
gauss_no_sub = []
exact_no_sub = exact_integral(f_y, y_start, y_end)

for n in N:
    trapezoid_no_sub.append(Trapez_integral(n, f_y, y_start, y_end))

    simpson_no_sub.append(Simpson_integral(n, f_y, y_start, y_end))

    gauss_no_sub.append(Gaus_quadratur_integral(f_y, y_start, y_end, n))

# ------------------------------------------------------------
# Numerische Integration mit Substitution
# ------------------------------------------------------------

trapezoid_sub = []
simpson_sub = []
gauss_sub = []
exact_sub = exact_integral(f_u, u_start, u_end)

for n in N:
    trapezoid_sub.append(Trapez_integral(n, f_u, u_start, u_end))

    simpson_sub.append(Simpson_integral(n, f_u, u_start, u_end))

    gauss_sub.append(Gaus_quadratur_integral(f_u, u_start, u_end, n))

# ------------------------------------------------------------
# Darstellung der Ergebnisse
# ------------------------------------------------------------

fig, ax = plt.subplots(1, 2, figsize=(12, 5), num = "Numerische Integration 1a)")
# --- Ohne Substitution ---------------------------------------

ax[0].plot(N, trapezoid_no_sub, label="Trapezregel")
ax[0].plot(N, simpson_no_sub, label="Simpsonregel")
ax[0].plot(N, gauss_no_sub, label="Gaußregel")

ax[0].hlines(exact_no_sub, 1, N_max, colors="k", linestyles="dashed", label="Exaktes Integral")

ax[0].set_xlabel("Anzahl der Intervalle")
ax[0].set_ylabel("Integralwert")
ax[0].set_title("Numerische Integration ohne Substitution")
ax[0].legend(loc="lower right")
ax[0].grid()


# --- Mit Substitution ----------------------------------------

ax[1].plot(N, trapezoid_sub, label="Trapezregel")
ax[1].plot(N, simpson_sub, label="Simpsonregel")
ax[1].plot(N, gauss_sub, label="Gaußregel")

ax[1].hlines(exact_sub, 1, N_max, colors="k", linestyles="dashed", label="Exaktes Integral")

ax[1].set_xlabel("Anzahl der Intervalle")
ax[1].set_ylabel("Integralwert")
ax[1].set_title("Numerische Integration mit Substitution")
ax[1].legend(loc="lower right")
ax[1].grid()

plt.tight_layout()
plt.savefig("1a).png")
# plt.show()

# endregion

# region Aufgabe 1b)

# Berechnet die Periode T(a) für drei Potentiale mit der Substitution
# x = a * (1 - u^2), die die Singularität am Umkehrpunkt beseitigt.
# Verglichen werden Trapez-, Simpson- und Gaußregel mit dem exakten Integral.

m = 1
n = 10

# Amplituden, für die T(a) berechnet wird
A = np.linspace(0.001, np.pi - 0.001, 100)

# Potentiale V(x)
V_x = [
    lambda x: np.cosh(x),
    lambda x: np.exp(np.abs(x)),
    lambda x: -np.cos(x)
]

# Substitution: x = a * (1 - u^2)

x = lambda u, a: a * (1 - u**2)
dx = lambda u, a: 2 * a * u

u_start = 0
u_end = 1

# Ergebnislisten (eine Kurve pro Potential)
T_a_trapezoid_all = []
T_a_simpson_all = []
T_a_gauss_all = []
T_a_exact_all = []

# Schleife über die Potentiale
for i, V in enumerate(V_x):

    T_a_trapezoid = []
    T_a_simpson = []
    T_a_gauss = []
    T_a_exact = []

    # Schleife über die Amplituden
    for a in A:

        # Grenzwert des Integranden bei u = 0 (dort 0/0)
        if i == 0:
            limit_value = 2 * np.sqrt(a / np.sinh(a))

        elif i == 1:
            limit_value = 2 * np.sqrt(a / np.exp(a))

        else:
            limit_value = 2 * np.sqrt(a / np.sin(a))

        def integrand(u):
            if u == 0:
                return limit_value

            return dx(u, a) / np.sqrt(V(a) - V(x(u, a)))
        
        T_a_trapezoid.append(Trapez_integral(n, integrand, u_start, u_end))
        T_a_simpson.append(Simpson_integral(n, integrand, u_start, u_end))
        T_a_gauss.append(Gaus_quadratur_integral(lambda u: dx(u, a) / np.sqrt(V(a) - V(x(u, a))), u_start, u_end, n))
        T_a_exact.append(exact_integral(integrand, u_start, u_end))

    T_a_trapezoid_all.append(np.array(T_a_trapezoid))
    T_a_simpson_all.append(np.array(T_a_simpson))
    T_a_gauss_all.append(np.array(T_a_gauss))
    T_a_exact_all.append(np.array(T_a_exact))


# Vorfaktor sqrt(8m) aus der Periodenformel
factor = np.sqrt(8 * m)

titles = [
    r"$V(x) = \cosh(x)$",
    r"$V(x) = e^{|x|}$",
    r"$V(x) = -\cos(x)$"
]

# Plot: T(a) für alle Methoden
fig, ax = plt.subplots(2, 2, figsize = [12,8])
ax = ax.flatten()

for i in range(len(V_x)):

    ax[i].plot(A, T_a_trapezoid_all[i] * factor, label="Trapezregel")
    ax[i].plot(A, T_a_simpson_all[i] * factor, label="Simpsonregel")
    ax[i].plot(A, T_a_gauss_all[i] * factor, label="Gaußregel")
    ax[i].plot(A, T_a_exact_all[i] * factor, label="Exaktes Integral")
    ax[i].set_xlabel("a")
    ax[i].set_ylabel("T(a)")
    ax[i].set_title(titles[i])

    ax[i].legend()
    ax[i].grid()

plt.savefig("1.1b).png")


# Plot: Abweichung der numerischen Integrale vom exakten Integral
fig, ax = plt.subplots(2, 2, num = "Abweichung der numerischen Integrale vom exakten Integral 1b)", figsize = [12,8])
ax = ax.flatten()
for i in range(len(V_x)):

    ax[i].plot(A,np.abs(T_a_trapezoid_all[i] * factor - T_a_exact_all[i] * factor), label="Trapezregel")
    ax[i].plot(A, np.abs(T_a_simpson_all[i] * factor - T_a_exact_all[i] * factor), label="Simpsonregel")
    ax[i].plot(A, np.abs(T_a_gauss_all[i] * factor - T_a_exact_all[i] * factor), label="Gaußregel")
    ax[i].set_xlabel("a")
    ax[i].set_ylabel("T(a)")
    ax[i].set_title(titles[i])
    ax[i].set_yscale("log")
    ax[i].legend()
    ax[i].grid()

plt.savefig("1.2b).png")

# plt.show()
# endregion

# region Aufgabe 1c)

# Sucht für verschiedene Potentialfamilien V(x, a1) mit V(0) = 0 und V(a) = 1
# den Formparameter a1, der das Verhältnis T(a) / T(a/2) maximiert.

a = 1  
precision = 10  
n = 100                  
V_a = 1                    
V_0 = V_a - 1

x = np.linspace(0, a, 1000)

# Beschriftungen der Potentiale (für Ausgabe und Legende)
V_x_txt = [
    "x^a1",
    "cosh(x*a1)",
    "1 - exp(-(a1 * x)²)",
    "-cos(a1 * x)",
    "tan(a1 * x)",
    "tanh(a1 * x)",
]

# Rohfunktionen f(x, a1); die Normierung erfolgt in normalize()
V_x = [
    lambda x, a1: x ** a1,
    lambda x, a1: np.cosh(a1 * x),
    lambda x, a1: 1 - np.exp(-(a1 * x)**2),            # Gauß-Topf
    lambda x, a1: -np.cos(a1 * x),
    lambda x, a1: np.tan(a1 * x),
    lambda x, a1: np.tanh(a1 * x),
]

# Untersuchter Bereich von a1 für jedes Potential
a1_range = [
    np.linspace(0.1, 1, n),
    np.linspace(0.1, 1, n),
    np.linspace(0.1, 6, n),                 # ab 6.2 geht es nicht mehr, da T_a2 so klein ist gegenüber dem Zähler, dass es als 0 gesehen wird
    np.linspace(0.1, np.pi - 1e-3, n),      # -cos: a1 < π, sonst nicht monoton auf [0, a]
    np.linspace(0.1, np.pi / 2 - 0.01, n),  # tan: Pol bei a1 = π/2
    np.linspace(0.1, 10, n),                # tanh: ab a1 ≈ 12 wird V(a) - V(x) numerisch 0 → inf
]

def normalize(f, a1, a):
    """V(0) = 0 und V(a) = 1 für beliebiges f(x, a1)"""
    f0, fa = f(0.0, a1), f(a, a1)
    return lambda x: (f(x, a1) - f0) / (fa - f0)

# Integrand der Periode: 1 / sqrt(V(a) - V(x))
def T_x(a, a1, V_x):
    return lambda x: 1 / np.sqrt(normalize(V_x, a1, a)(a) - normalize(V_x, a1, a)(x))

# Verhältnis der Integrale über [0, a] und [0, a/2]
def period_ratio(a, a1, V_x):
    return Gaus_quadratur_integral(T_x(a, a1, V_x), 0, a, precision) / Gaus_quadratur_integral(T_x(a / 2, a1, V_x), 0, a / 2, precision)

ratio_values = []
a1_best = []
ratio_best = []

plt.figure(num="Optimierung der Formparameter 1c)", figsize=(8,5))
print("\n 1c)")
# Schleife über die Potentiale: Verhältnis für alle a1 berechnen, bestes a1 wählen und plotten
for i in range(len(V_x)):
    a1_values = a1_range[i]
    V_function = V_x[i]

    ratio_values.append(np.array([period_ratio(a, a1, V_function) for a1 in a1_values]))
    best_a1_index = np.nanargmax(ratio_values[i])
    a1_best.append(a1_values[best_a1_index])
    ratio_best.append(ratio_values[i][best_a1_index])
    print(f"Best a1 für V(x) = {V_x_txt[i]}: {a1_best[i]:.4f} mit Verhältnis: {ratio_best[i]:.4f}")
    plt.plot(x, normalize(V_x[i], a1_best[i], a)(x), label=V_x_txt[i])

plt.xlabel("x")
plt.ylabel("V(x)")
plt.grid()
print("\n")
plt.legend()
plt.savefig("1c).png")

# endregion

# region Aufgabe 2a)

# Berechnet die Lage des Lagrange-Punkts L1 im Erde-Sonne-System als Nullstelle
# der Quintik (9) mit Bisektions- und Newtonverfahren und vergleicht die Konvergenz.

# --------------------------------------------------
# 3. Parameter des Erde-Sonne-Systems
# --------------------------------------------------

M_sun = 1.989e30
M_earth = 5.972e24
R = 1.496e11

mu = M_earth / (M_sun + M_earth)

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

x_bisection, steps_bisection = Bisektionsverfahren(f, 0, 1)
x_newton, steps_newton = Newtonverfahren(f, df, 1)

print("Bisektionsverfahren:")
print("x =", x_bisection)

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

error_bisection = np.abs(steps_bisection - x_ref)

error_newton = np.abs(steps_newton - x_ref)

# --------------------------------------------------
# 8. Diagramm: Konvergenzvergleich
# --------------------------------------------------

plt.figure(num="Konvergenzvergleich 2a)")

plt.semilogy(
    range(len(error_bisection)),
    error_bisection,
    "o-",
    label="Bisektionsverfahren"
)

plt.semilogy(
    range(len(error_newton)),
    error_newton,
    "o-",
    label="Newton-Verfahren"
)

plt.xticks(range(len(error_bisection)))
plt.xlabel("Iteration n")
plt.ylabel("Fehler |x_n - x_ref|")
plt.title("Konvergenzvergleich")
plt.legend()
plt.grid(True)
plt.savefig("2a).png")

# endregion

# region Aufgabe 2b)

# Überprüft die quadratische Konvergenz des Newton-Verfahrens, indem der
# Fehler e_(n+1) gegen e_n doppelt-logarithmisch aufgetragen wird.

# --------------------------------------------------
# 9. Quadratische Konvergenz des Newton-Verfahrens
# --------------------------------------------------

error = error_newton

# Fehler dürfen für die logarithmische Darstellung
# nicht null sein.

mask = ((error[:-1] > 0) & (error[1:] > 0))

e_n = error[:-1][mask]
e_n1 = error[1:][mask]

plt.figure(num="Quadratische Konvergenz des Newton-Verfahrens 2b)")

plt.loglog(e_n, e_n1, "o", label="Newton-Verfahren")

# Referenzkurve proportional zu e_n^2
if len(e_n) > 0:
    reference = e_n**2
    plt.loglog(e_n, reference, "--", label="Referenz: e_(n+1) ~ e_n^2")

plt.xlabel("Fehler e_n")
plt.ylabel("Fehler e_(n+1)")
plt.title("Überprüfung der quadratischen Konvergenz")
plt.legend()
plt.grid(True)
plt.savefig("2b).png")

# plt.show()
#endregion

# region Aufgabe 3a)

# Bonus: Zufallspolynome 6. Grades mit Koeffizienten in [0, 1]. Reelle Nullstellen
# in [-10, 10] werden über Vorzeichenwechsel und Bisektion gefunden, Nullstellen
# mit Abstand < root_precision gelten als gleich. Es wird die mittlere Anzahl
# der Nullstellen über mehrere Versuche bestimmt.

root_precision = 1e-4
trials = 10

num_roots = []

# Steuert, dass nur das erste Polynom geplottet wird
plotted = False


for _ in range(trials):
    # Zufällige Koeffizienten und Polynom samt Ableitung
    a = np.random.uniform(0, 1, 7)
    f = np.poly1d(a) 

    # Vorzeichenwechsel suchen und dort die Nullstelle per Bisektion bestimmen
    
    unique_roots = Zeros_in_Area(f,-10,10, root_precision)

    if plotted == False and len(unique_roots) != 0:
        plt.figure(num = "Verteilung der reellen Nullstellen 3a)")
        x_left, x_right = unique_roots[0] - 0.5, unique_roots[-1] + 0.5
        x_plot = np.abs(x_left - x_right)
        x_values = np.linspace(x_left, x_right ,np.int32(np.round(x_plot / root_precision)))
        plt.plot(x_values, f(x_values), label="Polynom")
        plt.plot(unique_roots, f(unique_roots), "ro", label="Nullstellen")
        plt.hlines(0, x_left, x_right, "k", label="x-Achse")
        plt.xlabel("Nullstelle x")
        plt.ylabel("Häufigkeit")
        plt.title("Verteilung der reellen Nullstellen")
        plotted = True

    num_roots.append(len(unique_roots))


print(f"Durchschnittliche Anzahl der reellen Nullstellen: {np.mean(num_roots):.2f}")
plt.savefig("3a).png")

plt.show()

# endregion