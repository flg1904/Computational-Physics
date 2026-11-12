import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

colors = ["green", "orange","cornflowerblue"]


Messung = pd.read_csv("1_zusammengefuehrt.csv", delimiter = ";")

E           = np.array(Messung["E / keV"].dropna().values)
n_lambda    = np.array(Messung["nlambda / pm"].dropna().values)
beta        = np.array(Messung["beta / °"].dropna().values)
R0          = np.array(Messung["R_0 / 1/s"].dropna().values)
R1          = np.array(Messung["R_1 / 1/s"].dropna().values)

lamb_MO = [71.080, 63.095]  # [Mo Ka, Mo Kb] in pm
E_MO = [17.479, 19.608]     # [Mo Ka, Mo Kb] in keV
beta_MO = [10.184, 9.030,20.7096,18.294]   # [Mo Ka, Mo Kb] in °


Plot3 = [[[E_MO[0],E_MO[0]],[0, max(R1[0:len(E)])]],
         [[E_MO[1],E_MO[1]],[0, max(R1[0:len(E)])]],
         [E, R1[0:len(E)]]]

Plot2 = [[[lamb_MO[0],lamb_MO[0]],[0, max(R1[0:len(n_lambda)])]],
         [[lamb_MO[1],lamb_MO[1]],[0, max(R1[0:len(n_lambda)])]],
         [[lamb_MO[0]*2,lamb_MO[0]*2],[0, max(R1[0:len(n_lambda)])]],
         [[lamb_MO[1]*2,lamb_MO[1]*2],[0, max(R1[0:len(n_lambda)])]],
         [n_lambda, R1[0:len(n_lambda)]]]


Plot1 = [[[beta_MO[0],beta_MO[0]],[0, max(R1[0:len(beta)])]],
         [[beta_MO[1],beta_MO[1]],[0, max(R1[0:len(beta)])]],
         [[beta_MO[2],beta_MO[2]],[0, max(R1[0:len(beta)])]],
         [[beta_MO[3],beta_MO[3]],[0, max(R1[0:len(beta)])]],
         [beta, R1[0:len(beta)]]]

xlabels = [r"$\vartheta$ / °", "nλ / pm", "E / keV"]
ylabels = [r"$R_1 \ / \ s^{-1} $", None, r"$R_1 \ / \ s^{-1} $"]
labels = [[r"$\vartheta_{Mo K_\alpha}$", r"$\vartheta_{Mo K_\beta}$", None, None, "Messwerte"],
           [r"$n\lambda_{Mo K_\alpha}$", r"$n\lambda_{Mo K_\beta}$",None, None, "Messwerte"],
           [r"$E_{Mo K_\alpha}$", r"$E_{Mo K_\beta}$", "Messwerte"]]
fmts = [["--", "--", "--","--", "-"],
        ["--", "--","--", "--", "-"],
        ["--", "--", "-"]]



Mehrere_Datenreihen_verschiedene_Plots(Plot1, Plot2, Plot3,
                                       xlabel_list = xlabels,
                                       ylabel_list = ylabels,
                                       labels_list = labels,
                                       fmtp_list = fmts,
                                       colors_list = [[colors[0], colors[1],colors[0],colors[1],colors[2]],
                                                      [colors[0], colors[1],colors[0],colors[1],colors[2]],
                                                      colors])

plt.show()


from scipy.signal import find_peaks

# Peaks in R1 suchen
peaks, properties = find_peaks(
    R1,
    prominence=30,  # Mindestprominenz – eventuell anpassen
    distance=3     # Mindestabstand zwischen Peaks in Messpunkten
)

# Zugehörige n_lambda-Werte bestimmen
n_lambda_peaks = n_lambda[peaks[1:]]
beta_peaks = beta[peaks[1:]]
print("Gefundene Peaks:")
for i, peak in enumerate(peaks[1:]):
    print(f"Peak {i+1}: nλ = {n_lambda_peaks[i]:.3f} pm")
    print(f"Peak {i+1}: β = {beta_peaks[i]:.3f} °")

d = n_lambda_peaks / (2 * np.sin(np.radians(beta_peaks)))
d_mean = csv_mittelwert(d)

print("\nBerechnete Gitterkonstanten d:")
for i, d_value in enumerate(d):
    print(f"d_{i+1} = {d_value:.3f} pm")
print(f" Mittelwert: d_mean = {d_mean:.3f} pm")



Plot2 = [[n_lambda, R1[0:len(n_lambda)]],[n_lambda_peaks, R1[peaks[1:]]]]

Plot1 = [[beta, R1[0:len(beta)]],[beta_peaks, R1[peaks[1:]]]]

xlabels = [r"$\vartheta$ / °", "nλ / pm"]
ylabels = [r"$R_1 \ / \ s^{-1} $", None]
labels = [["Messwerte", "Peaks"],
           ["Messwerte", "Peaks"]]
fmts = [["-","o"],
        ["-","o"]]



Mehrere_Datenreihen_verschiedene_Plots(Plot1, Plot2, 
                                       xlabel_list = xlabels,
                                       ylabel_list = ylabels,
                                       labels_list = labels,
                                       fmtp_list = fmts,
                                       colors_list = [[colors[-1], colors[1]],
                                                      [colors[-1], colors[1]]])

plt.show()