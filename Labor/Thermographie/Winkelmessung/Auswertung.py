import sys
from pathlib import Path

# Repo-Wurzel relativ zu dieser Datei bestimmen (parents[2] = zwei Ebenen höher)
repo_root = Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "Bibliotheken"))

from Fehlerberechnung import *
import numpy as np
import matplotlib.pyplot as plt


T_umgebung = ufloat(24 + 273, 0.5)

Messung2_2 = np.loadtxt("2.2_Winkelabhaengigkeit.csv", skiprows= 1, delimiter=";")

fehler_Winke = 0.5      # +/- 0.5 °
fehler_T = 0.4          # +/- 0.4 °C
Emissionsgrad = [0.32,0.98,0.96]


x_label = r"$\varphi$ / °"
y_label = "T / °C"
y_label2 = r"$\epsilon$ / 1"

labels_Plot1 = [[r"Messpunkte 1 $\epsilon_1 =$" + f"{Emissionsgrad[0]}", "T Referenz"], 
                [r"Messpunkte 2 $\epsilon_2 =$" + f"{Emissionsgrad[1]}", "T Referenz"], 
                [r"Messpunkte 3 $\epsilon_3 =$" + f"{Emissionsgrad[2]}", "T Referenz"]]

labels_Plot2 = [[r"$\epsilon_1$"], 
                [r"$\epsilon_2$"], 
                [r"$\epsilon_3$"]]
fmts = [["o","-"],
        ["o","-"],
        ["o","-"]]
colors = ["cornflowerblue", "orange"]
T_Parametrierung = [42.6,42.33,42.35]


Winkel = Messung2_2[:,0]

T_Oben = Messung2_2[:,1]
T_Mitte = Messung2_2[:,2]
T_Unten = Messung2_2[:,3]

Winkel = csv_data_plus_error(Winkel, fehler_Winke)
T_Oben = csv_data_plus_error(T_Oben, fehler_T)
T_Mitte = csv_data_plus_error(T_Mitte, fehler_T)
T_Unten = csv_data_plus_error(T_Unten, fehler_T)


Plot1 = [[[Winkel, T_Oben],[[0,80],[T_Parametrierung[0],T_Parametrierung[0]]]], 
        [[Winkel, T_Mitte],[[0,80],[T_Parametrierung[1],T_Parametrierung[1]]]], 
        [[Winkel, T_Unten],[[0,80],[T_Parametrierung[2],T_Parametrierung[2]]]]]

Mehrere_Datenreihen_verschiedene_Plots(Plot1[0],Plot1[1],Plot1[2],
                             xlabel_list= [x_label, x_label, x_label],
                             ylabel_list= [y_label, None, y_label],
                             labels_list= labels_Plot1,
                             fmtp_list= fmts,
                             colors_list=[colors,colors,colors],
                             grid_list=True,
                             error_list=[[True,False],[True,False],[True,False]],
                             sharey= True)
plt.show()

epsilon_phi1 = Emissionsgrad[0] * ((T_Oben+ 273) ** 4 - T_umgebung ** 4) /  ((T_Parametrierung[0]+ 273) ** 4 - T_umgebung ** 4)
epsilon_phi2 = Emissionsgrad[1] * ((T_Mitte+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[1]+ 273) ** 4 - T_umgebung ** 4)
epsilon_phi3 = Emissionsgrad[2] * ((T_Unten+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[2]+ 273) ** 4 - T_umgebung ** 4)

Plot1 = [[[Winkel, epsilon_phi1]], 
        [[Winkel, epsilon_phi2] ], 
        [[Winkel, epsilon_phi3] ]]

Mehrere_Datenreihen_verschiedene_Plots(Plot1[0],Plot1[1],Plot1[2],
                             xlabel_list= [None, None, x_label, x_label],
                             ylabel_list= [y_label2, None, y_label2, None],
                             labels_list= labels_Plot2,
                             fmtp_list= fmts,
                             colors_list=[colors,colors,colors,colors],
                             grid_list=True,
                             error_list=[[True,False],[True,False],[True,False],[True,False]])
plt.show()

Messung2_3 = np.loadtxt("2.3_Winkelabhaengigkeit_4Elemente.csv", skiprows= 1, delimiter= ";")
Emissionsgrad = [0.55,0.33,1,1]

x_label = r"$\varphi$ / °"
y_label = "T / °C"
labels_Plot1 = [[r"Messpunkte 4 $\epsilon_4 =$" + f"{Emissionsgrad[0]}", "T Referenz"], 
                [r"Messpunkte 5 $\epsilon_5 =$" + f"{Emissionsgrad[1]}", "T Referenz"], 
                [r"Messpunkte 6 $\epsilon_6 =$" + f"{Emissionsgrad[2]}", "T Referenz"],
                [r"Messpunkte 7 $\epsilon_7 =$" + f"{Emissionsgrad[3]}", "T Referenz"]]

labels_Plot2 = [[r"$\epsilon_4$"], 
                [r"$\epsilon_5$"], 
                [r"$\epsilon_6$"],
                [r"$\epsilon_7$"]]

fmts = [["o","-"],
        ["o","-"],
        ["o","-"],
        ["o","-"]]

T_Parametrierung = [51.0,52.5,44.8,24.8]
Emissionsgrad = [0.55,0.33,1,1]

Winkel = Messung2_3[:,0]

T_1 = Messung2_3[:,1]
T_2 = Messung2_3[:,2]
T_3 = Messung2_3[:,3]
T_4 = Messung2_3[:,4]

Winkel = csv_data_plus_error(Winkel, fehler_Winke)
T_1 = csv_data_plus_error(T_1, fehler_T)
T_2 = csv_data_plus_error(T_2, fehler_T)
T_3 = csv_data_plus_error(T_3, fehler_T)
T_4 = csv_data_plus_error(T_4, fehler_T)


Plot1 = [[[Winkel, T_1],[[0,80],[T_Parametrierung[0],T_Parametrierung[0]]]], 
        [[Winkel, T_2],[[0,80],[T_Parametrierung[1],T_Parametrierung[1]]]], 
        [[Winkel, T_3],[[0,80],[T_Parametrierung[2],T_Parametrierung[2]]]],
        [[Winkel, T_4],[[0,80],[T_Parametrierung[3],T_Parametrierung[3]]]]]

Mehrere_Datenreihen_verschiedene_Plots(Plot1[0],Plot1[1],Plot1[2],Plot1[3],
                             xlabel_list= [None, None, x_label, x_label],
                             ylabel_list= [y_label, None, y_label, None],
                             labels_list= labels_Plot1,
                             fmtp_list= fmts,
                             colors_list=[colors,colors,colors,colors],
                             grid_list=True,
                             error_list=[[True,False],[True,False],[True,False],[True,False]],
                             sharey= True)
plt.show()

T_Parametrierung = [51.0,52.5,46.8,44.8]

epsilon_phi1 = Emissionsgrad[0]  *((T_1+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[0]+ 273) ** 4 - T_umgebung ** 4)
epsilon_phi2 = Emissionsgrad[1]  *((T_2+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[1]+ 273) ** 4 - T_umgebung ** 4)
epsilon_phi3 = Emissionsgrad[2]  *((T_3+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[2]+ 273) ** 4 - T_umgebung ** 4)
epsilon_phi4 = Emissionsgrad[3]  *((T_4+ 273) ** 4 - T_umgebung ** 4) / ((T_Parametrierung[3]+ 273) ** 4 - T_umgebung ** 4)

Plot1 = [[[Winkel, epsilon_phi1]], 
        [[Winkel, epsilon_phi2] ], 
        [[Winkel, epsilon_phi3] ],
        [[Winkel, epsilon_phi4] ]]

Mehrere_Datenreihen_verschiedene_Plots(Plot1[0],Plot1[1],Plot1[2],Plot1[3],
                             xlabel_list= [None, None, x_label, x_label],
                             ylabel_list= [y_label2, None, y_label2, None],
                             labels_list= labels_Plot2,
                             fmtp_list= fmts,
                             colors_list=[colors,colors,colors,colors],
                             grid_list=True,
                             error_list=[[True,False],[True,False],[True,False],[True,False]])
plt.show()