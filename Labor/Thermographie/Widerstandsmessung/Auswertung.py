import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pan
import scipy.optimize as sc
from uncertainties import ufloat
from Fehlerberechnung import *

Text_size = 15
colors = ["cornflowerblue", "orange"]
# region 1.1

Delta_T = 0.4
Delta_t = 60

Ort_m = np.loadtxt("1.1_Ortsmessung.csv",skiprows= 1, delimiter= ",")
Zeit_m = pan.read_csv("1.1_Zeitmessung.csv",header= 0)

x_pix = Ort_m[:,0]
T_x = Ort_m[:,1]
T_x_mean = np.mean(T_x)
v_plot = [[min(x_pix), max(x_pix)], [T_x_mean,T_x_mean]]


t_s = np.array(Zeit_m["reltime"])
T_t = np.array(Zeit_m["T_mean"])

T_raum = T_t[0]

f_T_t = lambda t, tau, T_mean: T_raum + (T_mean-T_raum) * (1 - np.exp(- t / tau))

tau, T_max = fit_funktion(f_T_t,[t_s,T_t],[113, 35])
print(f"5 x tau: {tau*5:.2f} 1/s / W, T_max: {T_max:.2f} °C")



Mehrere_Datenreihen_verschiedene_Plots([[x_pix,T_x],v_plot],
                                       [[t_s,T_t],[t_s,f_T_t(t_s,tau.n, T_max.n)]],
                                       xlabel_list=["x / Pixel","t / s"],
                                       ylabel_list=[r"$T$ / °C",r"$T_{mean}$ / °C"],
                                       labels_list=[[r"$T(Pixel)$", r"$T_{mean}$"],
                                                    [r"$T_{mean}(t)$","T Fit"]],
                                       fmtp_list=[colors,colors], sharey= True,
                                       grid_list= True)

plt.show()

#endregion

# region 1.2

Messung = np.loadtxt("1.2_Messung.csv", skiprows = 1, delimiter = ";")

U_V = Messung[:,0]
I_mA = Messung[:,1]
T_C = Messung[:,2]

I_err = csv_data_plus_error(I_mA,I_mA * 0.01 + 0.03)
U_err = csv_data_plus_error(U_V,U_V * 0.0015 + 2 * 1e-4)
T_err = csv_data_plus_error(T_C, 0.5)


P_W = U_err * I_err * 1e-3

k, d, T_fit = lineare_Regression([P_W, T_err])
print(f"Steigung: {k:.2f} °C / W, Abstand: {d:.2f} °C")
plt.figure(figsize=(16, 7))
Mehrere_Datenreihen_ein_Plot([[P_W, T_err],T_fit], 
                             xlabel="P / W", 
                             ylabel= r"T / °C",
                             labels=[r"Messpunkte", r"linearer Fit"],
                             fmtp=["o","-"],
                             grid= True, 
                             error= [True, False],
                             markerwiths= None)

plt.show()


# endregion