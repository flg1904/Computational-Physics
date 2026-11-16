import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

colors = ["green", "orange", "cornflowerblue"]


# ============================================================
# 1. Messdaten einlesen
# ============================================================

Kalibrierung = pd.read_csv("Halleffekt_Kalibrierung.csv")
Messung = pd.read_csv("Halleffekt_Messreihe.csv")

# Kalibrierungsmessung
I_M = Kalibrierung.iloc[:, 0].to_numpy()       # A
B_Kal = Kalibrierung.iloc[:, 1].to_numpy()     # mT

# Hall-Messung
B = Messung.iloc[:, 0].to_numpy() * 1e-3       # mT -> T
I_S = Messung.iloc[:, 1].to_numpy() * 1e-3     # mA -> A
U_H = Messung.iloc[:, 2].to_numpy() * 1e-3     # mV -> V

# Probendicke
d = 1e-3                                      # m

# Elementarladung
e = 1.602176634e-19


# ============================================================
# 2. Kalibrierung des Magnetfeldes
# ============================================================

# Lineare Regression: B = a * I_M + b
Steigung_Kal, Achsenabschnitt_Kal, Fit_Kal = lineare_Regression(
    [I_M, B_Kal]
)

print("\n========== MAGNETFELDKALIBRIERUNG ==========")
print(f"Steigung:            {Steigung_Kal} mT/A")
print(f"Achsenabschnitt:     {Achsenabschnitt_Kal} mT")

# Diagramm
plt.figure(figsize=(9, 6))

Plot_Datenreihe(
    [I_M, B_Kal],
    titel="Kalibrierung des Magnetfeldes",
    xlabel=r"Spulenstrom $I_M$ / A",
    ylabel=r"Magnetische Flussdichte $B$ / mT",
    fmtp="o",
    color_line=colors[0],
    label="Messwerte",
    grid=True
)

Plot_Datenreihe(
    Fit_Kal,
    fmtp="-",
    color_line=colors[1],
    label="Lineare Regression"
)

plt.tight_layout()
plt.savefig("Kalibrierung_Magnetfeld.png", dpi=300)
plt.show()


# ============================================================
# 3. Offset-Korrektur der Hallspannung
# ============================================================

# Messwerte bei B = 0 auswählen
Maske_Offset = np.isclose(B, 0)

I_Offset = I_S[Maske_Offset]
U_Offset = U_H[Maske_Offset]

# Offsetgerade: U_Offset = a * I_S + b
Steigung_Offset, Achsenabschnitt_Offset, Fit_Offset = lineare_Regression(
    [I_Offset, U_Offset]
)

print("\n========== OFFSET-KORREKTUR ==========")
print(f"Offset-Steigung:        {Steigung_Offset} V/A")
print(f"Offset-Achsenabschnitt: {Achsenabschnitt_Offset} V")

# Offset für jeden Messpunkt berechnen
U_Offset_berechnet = (
    Steigung_Offset.nominal_value * I_S
    + Achsenabschnitt_Offset.nominal_value
)

# Offset von der Hallspannung abziehen
U_H_korr = U_H - U_Offset_berechnet


# Diagramm der Offsetmessung
plt.figure(figsize=(9, 6))

Plot_Datenreihe(
    [I_Offset * 1e3, U_Offset * 1e3],
    titel="Bestimmung des Hallspannungs-Offsets",
    xlabel=r"Querstrom $I_S$ / mA",
    ylabel=r"Hallspannung $U_H$ / mV",
    fmtp="o",
    color_line=colors[0],
    label="Messwerte bei B = 0",
    grid=True
)

# Fitwerte für die Darstellung in mA und mV umrechnen
Fit_Offset_plot = [
    Fit_Offset[0] * 1e3,
    Fit_Offset[1] * 1e3
]

Plot_Datenreihe(
    Fit_Offset_plot,
    fmtp="-",
    color_line=colors[1],
    label="Lineare Regression"
)

plt.tight_layout()
plt.savefig("Offset_Hallspannung.png", dpi=300)
plt.show()


# ============================================================
# 4. Hallspannung als Funktion des Querstroms
# ============================================================

# Verschiedene Magnetfeldwerte bestimmen
B_Werte = np.sort(np.unique(B))

Datenreihen_Hall = []
Labels_Hall = []

for B_Wert in B_Werte:

    Maske = np.isclose(B, B_Wert)

    I_plot = I_S[Maske]
    U_plot = U_H_korr[Maske]

    # Nach Querstrom sortieren
    Sortierung = np.argsort(I_plot)

    I_plot = I_plot[Sortierung]
    U_plot = U_plot[Sortierung]

    Datenreihen_Hall.append([
        I_plot * 1e3,
        U_plot * 1e3
    ])

    Labels_Hall.append(
        f"B = {B_Wert * 1e3:.1f} mT"
    )


# Für jede Messreihe eine eigene Farbe erzeugen
Farben = plt.get_cmap("viridis")(
    np.linspace(0, 1, len(B_Werte))
).tolist()


plt.figure(figsize=(11, 8))

Mehrere_Datenreihen_ein_Plot(
    data_list=Datenreihen_Hall,
    titel="Hallspannung in Abhängigkeit vom Querstrom",
    xlabel=r"Querstrom $I_S$ / mA",
    ylabel=r"Korrigierte Hallspannung $U_H$ / mV",
    fmtp="o-",
    error=False,
    grid=True,
    labels=Labels_Hall,
    colors=Farben,
    linewidths=1.5,
    markersizes=5
)

plt.tight_layout()
plt.savefig("Hallspannung_Querstrom.png", dpi=300)
plt.show()


# ============================================================
# 5. Bestimmung der Hallkonstante
# ============================================================

# Zusammenhang:
#
# U_H = R_H * I_S * B / d
#
# Umformen:
#
# U_H / I_S = R_H * B / d
#
# x = B / d
# y = U_H / I_S
#
# Die Steigung entspricht R_H.

x = B / d
y = U_H_korr / I_S

# Regression durch den Ursprung
R_H, Achsenabschnitt_Hall, Fit_Hall = lineare_Regression(
    [x, y],
    durch_ursprung=True
)

print("\n========== HALLKONSTANTE ==========")
print(f"Hallkonstante R_H: {R_H} m³/C")


# Diagramm
plt.figure(figsize=(9, 6))

Plot_Datenreihe(
    [x, y],
    titel="Bestimmung der Hallkonstante",
    xlabel=r"$B/d$ / T/m",
    ylabel=r"$U_H/I_S$ / $\Omega$",
    fmtp="o",
    color_line=colors[0],
    label="Messwerte",
    grid=True
)

Plot_Datenreihe(
    Fit_Hall,
    fmtp="-",
    color_line=colors[1],
    label="Regression durch den Ursprung"
)

plt.tight_layout()
plt.savefig("Hallkonstante.png", dpi=300)
plt.show()


# ============================================================
# 6. Ladungsträgerkonzentration
# ============================================================

# Für überwiegende Elektronen- oder Löcherleitung:
#
# |R_H| = 1 / (n * e)
#
# Daraus:
#
# n = 1 / (e * |R_H|)

n = 1 / (e * abs(R_H))

print("\n========== LADUNGSTRÄGERKONZENTRATION ==========")
print(f"Ladungsträgerkonzentration: {n} 1/m³")
print(f"Ladungsträgerkonzentration: {n * 1e-6} 1/cm³")

# Vorzeichen auswerten
if R_H.nominal_value < 0:
    print("Negatives Vorzeichen: Elektronenleitung (n-Leitung).")
else:
    print("Positives Vorzeichen: Löcherleitung (p-Leitung).")
