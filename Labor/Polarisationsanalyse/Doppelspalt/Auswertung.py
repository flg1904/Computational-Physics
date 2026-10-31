import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np

Messung = np.loadtxt("Beugungsmaxima.csv", skiprows= 1, delimiter= ";")

error_r = 0.5               # Fehler der Radialen Messung in mm

k = Messung[:, 0]           # Ordnung des Beugungsmaxima
r = [Messung[:, 1],         # Radialer Abstand zur Nullten Ordnung
     Messung[:, 2],
     Messung[:, 3],
     Messung[:, 4],]
l = 2510                    # Abstand zum Schirm in mm
d = [0.25, 0.25, 0.5, 1]    # Spaltabstand in mm

# for i in range(len(r)):
#     r[i] = csv_data_plus_error(r[i], error_r)

sin_alpha = [r_i / np.sqrt(r_i**2 + l**2) for r_i in r]

lambda_laser = [d[ind] * asin_alpha_i / k for ind, asin_alpha_i in enumerate(sin_alpha)]
lambda_mean = [csv_mittelwert(lambda_laser_i * 1e6) for lambda_laser_i in lambda_laser]
lambda_mean_ges = csv_mittelwert(np.hstack(lambda_laser) * 1e6)
lambda_mean_ges_ohne4 = csv_mittelwert(np.hstack(lambda_laser[0:-1]) * 1e6)

print(f"Lambda 1                 =     ({lambda_mean[0]:.0f}) nm")
print(f"Lambda 2                 =     ({lambda_mean[1]:.0f}) nm")
print(f"Lambda 3                 =     ({lambda_mean[2]:.0f}) nm")
print(f"Lambda 4                 =    ({lambda_mean[3]:.0f}) nm")
print( "--------------------------------------------")
print(f"Lambda Gesamt            =     ({lambda_mean_ges:.0f}) nm")
print(f"Lambda Gesamt ohne 4     =     ({lambda_mean_ges_ohne4:.0f}) nm")


r = Messung[:, 5]         # Radialer Abstand zur Nullten Ordnung

# for i in range(len(r)):
#     r[i] = csv_data_plus_error(r[i], error_r)

sin_alpha = r / np.sqrt(r**2 + l**2)

d = lambda_mean_ges.n * 1e-3* k / sin_alpha
d_ohne4 = lambda_mean_ges_ohne4.n * 1e-3* k / sin_alpha

d_mean = csv_mittelwert(d)
d_ohne4_mean = csv_mittelwert(d_ohne4)
print( "--------------------------------------------")
print(f"Gitterkonsatante:        = ({d_mean:.1f}) µm")
print(f"Gitterkonsatante ohne 4: = ({d_ohne4_mean:.1f}) µm")
