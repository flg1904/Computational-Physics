import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

Messungen = pd.read_csv("2a.csv", sep = ";", decimal = ".")

beta          = np.array(Messungen["beta / °"].values)
R_0           = np.array(Messungen["R_0 / 1/s"].values)
R_1           = np.array(Messungen["R_1 / 1/s"].values)
R_2           = np.array(Messungen["R_2 / 1/s"].values)
R_3           = np.array(Messungen["R_3 / 1/s"].values)
R_4           = np.array(Messungen["R_4 / 1/s"].values)
R_5           = np.array(Messungen["R_5 / 1/s"].values)
R_6           = np.array(Messungen["R_6 / 1/s"].values)

R_0_m = ~np.isnan(R_0)
R_1_m = ~np.isnan(R_1)
R_2_m = ~np.isnan(R_2)
R_3_m = ~np.isnan(R_3)
R_4_m = ~np.isnan(R_4)
R_5_m = ~np.isnan(R_5)
R_6_m = ~np.isnan(R_6)

Plot_R = [
    [beta[R_0_m], R_0[R_0_m]],
    [beta[R_1_m], R_1[R_1_m]],
    [beta[R_2_m], R_2[R_2_m]],
    [beta[R_3_m], R_3[R_3_m]],
    [beta[R_4_m], R_4[R_4_m]],
    [beta[R_5_m], R_5[R_5_m]],
    [beta[R_6_m], R_6[R_6_m]],
]

# Plot-Einstellungen: Reihenfolge entspricht R_0 bis R_6 in Plot_R.
titel_R = None
xlabel_R = r"$\vartheta$ / °"
ylabel_R = r"$R_i$ / s$^{-1}$"
labels_R = [r"$R_0$", r"$R_1$", r"$R_2$", r"$R_3$", r"$R_4$", r"$R_5$", r"$R_6$"]
fmtp_R = ["o-", "o-", "o-", "o-", "o-", "o-", "o-"]
colors_R = [
    "green",
    "orange",
    "cornflowerblue",
    "red",
    "purple",
    "brown",
    "gray",
]
linewidths_R = [2] * 7
markersizes_R = [6] * 7
markerwiths_R = [1] * 7
grid_R = True
leg_loc_R = "best"
label_sizes_R = (24, 24, 30)
plt.figure(figsize=(12, 6))
Mehrere_Datenreihen_ein_Plot(
    Plot_R,
    titel=titel_R,
    xlabel=xlabel_R,
    ylabel=ylabel_R,
    labels=labels_R,
    fmtp=fmtp_R,
    colors=colors_R,
    linewidths=linewidths_R,
    markersizes=markersizes_R,
    markerwiths=markerwiths_R,
    grid=grid_R,
    leg_loc=leg_loc_R,
    label_sizes=label_sizes_R,
)

plt.tight_layout()
# plt.show()

# Fit-Bereiche als Indizes innerhalb der jeweils vorhandenen Messwerte.
# Der Endindex ist inklusive; None bedeutet den letzten Messpunkt.
fit_start_R = [10, 3, 2, 6, 10, 5, 5]
fit_end_R = [19, 10, 10, 12, 15, 12, 13]

fit_parameter_R = []
Plot_Fit = Plot_R.copy()
labels_Fit = [None for label in labels_R]
fmtp_Fit = ["o"] * len(Plot_R)
colors_Fit = colors_R.copy()
theta = []


for i, (beta_R, rate_R) in enumerate(Plot_R):
    start = fit_start_R[i]
    end = fit_end_R[i]
    stop = len(beta_R) if end is None else end + 1

    if start < 0 or stop > len(beta_R) or start >= stop:
        raise ValueError(f"Ungültiger Fit-Bereich für R_{i}: {start} bis {end}.")

    fit_data = [beta_R[start:stop], rate_R[start:stop]]
    if len(fit_data[0]) < 3:
        raise ValueError(f"Der Fit-Bereich für R_{i} muss mindestens 3 Punkte enthalten.")

    steigung, achsenabschnitt, _ = lineare_Regression(fit_data)
    if steigung.nominal_value == 0:
        raise ValueError(f"Die Steigung des linearen Fits für R_{i} ist null.")

    theta_null = -achsenabschnitt / steigung
    theta.append(theta_null.nominal_value)
    print(f"R_{i}: Fit-Nullstelle bei theta = {theta_null:.3f}°")
    fit_parameter_R.append((steigung, achsenabschnitt))

    beta_fit = np.linspace(theta_null, fit_data[0][-1], 300)
    rate_fit = steigung.nominal_value * beta_fit + achsenabschnitt.nominal_value
    Plot_Fit.append([beta_fit, rate_fit])
    labels_Fit.append("Lineare Fits" if i == 0 else None)
    fmtp_Fit.append("--")
    colors_Fit.append("black")

plt.figure(figsize=(12, 6))
Mehrere_Datenreihen_ein_Plot(
    Plot_Fit,
    titel=None,
    xlabel=xlabel_R,
    ylabel=ylabel_R,
    labels=labels_Fit,
    fmtp=fmtp_Fit,
    colors=colors_Fit,
    linewidths=[2] * len(Plot_Fit),
    markersizes=[6] * len(Plot_Fit),
    markerwiths=[1] * len(Plot_Fit),
    grid=grid_R,
    leg_loc=leg_loc_R,
    label_sizes=label_sizes_R,
)

plt.tight_layout()
plt.show()


E_max = np.array([22, 24, 26, 28, 30, 33, 35]) # Maximal energies in keV
d_mean = ufloat(201.338, 0.018) * 1e-12

c = 299792458 # m/s
h = E_max * 2 * d_mean * np.sin(np.radians(np.array(theta)+ 0.5))/ c
print(f"Berechnete Planck-Konstanten h: {csv_mittelwert(Ufloat_to_array(h))}")