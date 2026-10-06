import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integral

def Trapez_integral(n, f_x, x_start, x_end):
    """
        Berechen das Integral von f(x) über das Intervall [x[0], x[-1]] mit der Trapezregel.

        Parameters
        ----------
        n : int
            Die Anzahl der Intervalle, in die das Intervall [x[0], x[-1]] unterteilt wird.
        f_x : lambda function
            Die Funktion f(x), die integriert werden soll.
        x_start : float
            Der Startwert des Intervalls.
        x_end : float
            Der Endwert des Intervalls.
    """
    integral = 0
    delt_x = (x_end - x_start) / n

    for ind in range(n):
        a = f_x(x_start + ind * delt_x)
        b = f_x(x_start + (ind + 1) * delt_x)

        integral += delt_x * (a + b) / 2

    return integral

def Simpson_integral(n, f_x, x_start, x_end):
    """
        Berechen das Integral von f(x) über das Intervall [x[0], x[-1]] mit der Simpsonregel.

        Parameters
        ----------
        n : int
            Die Anzahl der Intervalle, in die das Intervall [x[0], x[-1]] unterteilt wird.
        f_x : lambda function
            Die Funktion f(x), die integriert werden soll.
        x_start : float
            Der Startwert des Intervalls.
        x_end : float
            Der Endwert des Intervalls.
    """
    integral = 0
    delt_x = (x_end - x_start) / n

    for ind in range(0, n - 2, 2):
        a = f_x(x_start + ind * delt_x)
        b = f_x(x_start + (ind + 1) * delt_x)
        m = f_x(x_start + (ind + 0.5) * delt_x)

        integral += delt_x * (a + 4 * m + b) / 3

    return integral

def Gaus_integral(n, f_x, x_start, x_end):
    """
        Berechen das Integral von f(x) über das Intervall [x[0], x[-1]] mit der Gaußregel.

        Parameters
        ----------
        n : int
            Die Anzahl der Intervalle, in die das Intervall [x[0], x[-1]] unterteilt wird.
        f_x : lambda function
            Die Funktion f(x), die integriert werden soll.
        x_start : float
            Der Startwert des Intervalls.
        x_end : float
            Der Endwert des Intervalls.
    """
    integral = 0
    delt_x = (x_end - x_start) / n

    for ind in range(n):
        a = f_x(x_start + (ind+ 0.5) * delt_x)


        integral += delt_x * a

    return integral

def exact_integral(f_x, x_start, x_end):
    """
        Berechen das exakte Integral von f(x) über das Intervall [x[0], x[-1]].

        Parameters
        ----------
        f_x : lambda function
            Die Funktion f(x), die integriert werden soll.
        x_start : float
            Der Startwert des Intervalls.
        x_end : float
            Der Endwert des Intervalls.
    """
    return integral.quad(f_x, x_start, x_end)[0]


lambda_f = lambda x: np.sin(x)  # Funktion, die integriert werden soll
N_max = 10  # Maximale Anzahl der Intervalle
N = np.arange(1, N_max + 1)

Trapez = []
Simpson = []
Gaus = []
exact = exact_integral(lambda_f, 0, np.pi)

for n in N:
    Trapez.append(Trapez_integral(n, lambda_f, 0, np.pi))
    Simpson.append(Simpson_integral(n, lambda_f, 0, np.pi))
    Gaus.append(Gaus_integral(n, lambda_f, 0, np.pi))

plt.figure()
plt.plot(N, np.array(Trapez), label='Trapezregel')
plt.plot(N, np.array(Simpson), label='Simpsonregel')
plt.plot(N, np.array(Gaus), label='Gaußregel')
plt.hlines(exact, 1, N_max, colors='k', linestyles='dashed', label='Exaktes Integral')
plt.xlabel('Anzahl der Intervalle')
plt.ylabel('Absoluter Fehler')
plt.title('Absoluter Fehler der Integrationsmethoden')
plt.legend()

plt.show()