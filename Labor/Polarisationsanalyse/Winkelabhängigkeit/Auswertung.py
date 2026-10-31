import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import matplotlib.pyplot as plt

Messung = np.loadtxt("Transmissionen.csv", skiprows= 1, delimiter=";")

phi = Messung[:,0]
I = Messung[:,1]
I_2 = Messung[-3,2]
phi_2 = Messung[-3,0]

err_phi = 2 
err_I = I * 0.001 + 1
phi_e = csv_data_plus_error(phi, err_phi) / 180 *np.pi
I_e = csv_data_plus_error(I, err_I)
phi = np.linspace(0,np.pi, 100)

Plot = [phi_e, I_e]


I_fit = lambda phi, I_0, del_phi: I_0 * np.cos(phi + del_phi)**2 

parameter = fit_funktion(I_fit, Plot, [600, 1] )
I_fit_werte = I_fit(phi , parameter[0].n, parameter[1].n)

print(f"I_0:      {parameter[0]:.1f}       lx")
print(f"delt phi:   {parameter[1]:.4f} rad")
print(f"delt phi: {parameter[1]/ np.pi * 180:.2f}     °")

plt.figure( figsize = (12, 8))
Mehrere_Datenreihen_ein_Plot([Plot, [phi, I_fit_werte],[[phi_e[-3]],[I_2]]],
                              xlabel = r"$\varphi$ / rad",
                              ylabel = "I / lx",
                              fmtp   = ["o","-", "o"],
                              error  = [True, False, True],
                              grid   = True,
                              labels = ["Datenpunkte", "Fit", "Mit Polarisatiosfolie"],
                              markersizes = 6)

plt.xticks(
    [0, np.pi/2, np.pi],
    [r"$0$", r"$\pi / 2$", r"$\pi$"]
)
plt.show()