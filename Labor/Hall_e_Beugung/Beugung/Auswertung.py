import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from uncertainties.umath import sqrt

colors = ["green", "orange","cornflowerblue"]

Data = np.loadtxt("Elektronenbeugung1.csv", delimiter=",", skiprows=1)

U = Data[:, 0]  * 1e3  # Spannung in V
D1 = Data[:, 1] * 1e-3 # in m
D2 = Data[:, 2] * 1e-3 # in m

e = 1.602176634e-19  # Elementarladung in Coulomb
me = 9.10938356e-31  # Elektronenmasse in kg
h = 6.62607015e-34  # Plancksches Wirkungsquantum in Js

R = ufloat(6.75, 0.05) * 1e-2 # in m

U_e = csv_data_plus_error(U, 0.01 * U + 1)  # Fehler in V
D1_e = csv_data_plus_error(D1, 0.5 * 1e-3)  # Fehler in m
D2_e = csv_data_plus_error(D2, 0.5 * 1e-3)  # Fehler in m


lam = [h / sqrt(2 * me * e * u) for u in U_e]  # Wellenlänge in m

x_Achs1 = D1_e / 2
y_Achs1 = np.array([2 * R * lam_i for lam_i in lam])

x_Achs2 = D2_e / 2
y_Achs2 = np.array([2 * R * lam_i for lam_i in lam])

steigung1, achsenabschnitt1, fit1 = lineare_Regression(
    [x_Achs1, y_Achs1]
)
steigung2, achsenabschnitt2, fit2 = lineare_Regression(
    [x_Achs2, y_Achs2]
)

print(f"d1: {steigung1 * 1e12} pm")
print(f"d2: {steigung2 * 1e12} pm")


Mehrere_Datenreihen_verschiedene_Plots(
    [ [x_Achs1 * 1e3, y_Achs1* 1e12], [fit1[0]* 1e3, fit1[1]* 1e12] ],
     [ [x_Achs2 * 1e3, y_Achs2* 1e12], [fit2[0]* 1e3, fit2[1]* 1e12] ],
    xlabel_list=[r"$D_1 / 2$ / mm", r"$D_2 / 2$ / mm"],
    ylabel_list=[r"$2R\lambda$ / pm", None],
    labels_list=[
        ["Messpunkte D1", "Linearer Fit"],
        ["Messpunkte D2", "Linearer Fit"],
    ],
    fmtp_list=[["o", "-"], ["o", "-"]],
    colors_list=[
        [colors[0], colors[1]],
        [colors[2], colors[1]],
    ],
    grid_list=True,
    error_list = [[True, False], [True, False]]
)



Data = np.loadtxt("Elektronenbeugung2.csv", delimiter=",", skiprows=1)

U    = Data[:, 0]  * 1e3        # Spannung in V
I    = Data[:, 1] * 1e-3        # in A
B    = Data[:, 2] * 1e-3        # in T
s    = Data[:, 3] * 1e-3        # in m
d    = 136 * 1e-3               # in m
mu_0 = 4 * np.pi * 1e-7         # in T*m/A
R    = ufloat(68, 4) * 1e-3     # Spulenradius in m
a    = R / 2                    # halber Spulenradiusin m 
n    = ufloat(320, 10)          # Windungszahl

s_e = csv_data_plus_error(s, 1 * 1e-3)  # Fehler in m
I_e = csv_data_plus_error(I, I * 0.001 + 0.04 * 1e-3)  # Fehler in A
B_e = csv_data_plus_error(B, 0.1 * 1e-3)  # Fehler in T
U_e = csv_data_plus_error(U, 10)  # Fehler in V

sin_alpha = s_e / d
l = np.sqrt(d**2 - s**2)

r = l / (2 * sin_alpha)
B_r_e = mu_0 * (n * R**2 * I_e) / (R**2 + a**2)**(3/2)


for ind, r_ in enumerate(r):
    print(f"r{ind+1}: {r_ * 1e3} mm", 
          f";B berechnet{ind+1}: {B_r_e[ind] * 1e3:.2f} mT", 
          f";B gemessen{ind+1}: {B_e[ind] * 1e3:.2f} mT")

x_Achs = B_e / np.sqrt(U)
y_Achs = 1 / r
Plot = [x_Achs, y_Achs]

steigung, achsenabschnitt, fit = lineare_Regression(
    [x_Achs, y_Achs], True
)


print(f"e / m_e: {2 * steigung**2}, Offset: {achsenabschnitt}")


Mehrere_Datenreihen_verschiedene_Plots(
    [ [x_Achs, y_Achs], [fit[0], fit[1]] ],
    xlabel_list=[r"$B / \sqrt{U} \ / \ T \ V^{-1/2}$"],
    ylabel_list=[r"$1 / r \ / \ m^{-1}$"],
    labels_list=[
        ["Messpunkte", "Linearer Fit"]
    ],
    fmtp_list=[["o", "-"]],
    colors_list=colors,
    grid_list=True,
    error_list = [[True, False]]
)

plt.show()
