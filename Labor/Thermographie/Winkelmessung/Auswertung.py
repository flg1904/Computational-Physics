import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import matplotlib.pyplot as plt

Messung2_2 = np.loadtxt("2.2_Winkelabhaengigkeit.csv", skiprows= 1, delimiter=";")
Messung2_3 = np.loadtxt("2.3_Winkelabhaengigkeit_4Elemente.csv", skiprows= 1, delimiter= ";")

fehler_Winke = 0.5      # +/- 0.5 °
fehler_T = 0.4          # +/- 0.4 °C


x_label = r"$\varphi$ / °"
y_label = "T / °C"
labels_Plot1 = ["T Oben", "T Mitte", "T Unten"]
colors = ["cornflowerblue", "orange", "green"]



Winkel = Messung2_2[:,0]

T_Oben = Messung2_2[:,1]
T_Mitte = Messung2_2[:,2]
T_Unten = Messung2_2[:,3]

Winkel = csv_data_plus_error(Winkel, fehler_Winke)
T_Oben = csv_data_plus_error(T_Oben, fehler_T)
T_Mitte = csv_data_plus_error(T_Mitte, fehler_T)
T_Unten = csv_data_plus_error(T_Unten, fehler_T)


Plot1 = [[Winkel, T_Oben], [Winkel, T_Mitte], [Winkel, T_Unten]]
plt.figure(figsize=(16, 7))
Mehrere_Datenreihen_ein_Plot(Plot1,
                             xlabel= x_label,
                             ylabel= y_label,
                             labels= labels_Plot1,
                             fmtp= "o",
                             colors = colors,
                             grid = True,
                             error=True,
                             markerwiths= 3)
plt.show()