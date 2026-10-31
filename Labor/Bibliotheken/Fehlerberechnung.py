from uncertainties import ufloat
import numpy as np
from uncertainties import unumpy as unp
import matplotlib.pyplot as plt
from uncertainties.core import UFloat, Variable
import scipy.interpolate as sci
import scipy.optimize as opt
import math

def csv_data_plus_error(data, error):
    """
    Erstelle ein Array aus den Daten und Fehlern.
    :param data: Array mit den Daten
    :param error: Array mit den Fehlern
    :return: Array mit den Daten und Fehlern
    """
    if not isinstance(error, list) and not isinstance(error, np.ndarray):
        error = [error] * len(data)

    

    return np.array([ufloat(d, e) for d, e in zip(data, error)])

def Ufloat_to_array(data):
    """
    Konvertiert eine Liste von UFloat-Objekten 
    (diese Liste kann auch aus gemischten datentypen bestehen) in ein NumPy-Array.
    :param data: Liste von UFloat-Objekten
    :return: NumPy-Array mit den nominalen Werten der UFloat-Objekte
    """
    arry = np.zeros_like(data, dtype=float)

    if isinstance(data, (list, np.ndarray)):
        for i, d in enumerate(data):
            if isinstance(d, UFloat):
                arry[i] = d.nominal_value
            elif isinstance(d, (int, float, Variable)):
                arry[i] = d
        return arry
    else:
        raise ValueError("Input must be a list or a NumPy array of UFloat objects.")

def csv_mittelwert(data, mode = True):
    """
    Berechne die Standardabweichung der Daten.
    :param data: Liste mit Arrays der Daten
    :return: 
        1) Mittelwert als ufloat, 
        2) Mittelwert, 
        3) Standardabweichung, 
        4) Standardabweichung des Mittelwerts
    """
    Mittel = []
    Sigma = []
    Sigma_Mittel = []
    Mittel_ufloat = []

    if not isinstance(data[0], list):
        data = [data]
    

    for i, d in enumerate(data):
        Mittel.append(np.mean(d))
        if(len(d) == 1):
            Sigma.append(None) 
            Sigma_Mittel.append(None)
        else:
            Sigma.append(np.sqrt(1/ (len(d) - 1) * np.sum((d - Mittel[i]) ** 2)))
            Sigma_Mittel.append(Sigma[i] / np.sqrt(len(d)))
            Mittel_ufloat.append(ufloat(Mittel[i], Sigma_Mittel[i]))
            
    if mode: 
        return Mittel_ufloat[0]
    
    return Mittel_ufloat, Mittel, Sigma, Sigma_Mittel

def mean_ufloat_explicit(values):
    """
    Mittelwert aus nominalen Werten und Fehlern.
    Fehler des Mittelwerts: sqrt(sum(sigma_i^2)) / N
    """
    if len(values) == 0:
        raise ValueError("Leere Liste kann nicht gemittelt werden.")

    vals = unp.nominal_values(values)
    errs = unp.std_devs(values)

    mean_val = np.mean(vals)
    mean_err = np.sqrt(np.sum(errs**2)) / len(values)

    return ufloat(mean_val, mean_err)

def Plot_Datenreihe(data, titel = None, xlabel = "x-Achse", 
                    ylabel = "y-Achse", fmtp='-', 
                    error=False, grid=False, label=None, 
                    interpolation="linear", leg_loc="best",
                    label_sizes = (24,24,30), linewidth=2,
                    markersize = 10, markerwidth = 2,
                    color_line = None):

    """
    Plotte eine Datenreihe.
    :param data: Array mit den Daten
        Erster Eintrag: x-Werte,
        Zweiter Eintrag: y-Werte,
        Dritter Eintrag: Fehler in y-Richtung (optional)
        Vierter Eintrag: Fehler in x-Richtung (optional)
    :param Parameter: Enthält die Plot Parameter 
        1) Titel des Plots,
        2) x-Achsenbeschriftung,
        3) y-Achsenbeschriftung
        4) Grafikeinmstellung (optional) (farben, Linienstile, Marker, etc.),
        5) Fehlerbalken (bool)
        6) Legende (bool)
        7) Grid (bool)
        8) Label der Legende (optional)
        9) Interpolation (optional, Standard: "linear", "cubic","nearest", "quadratic")
        10) Legendenposition (optional, Standard: "upper right")
        11) Labelgrößen (optional, Standard: (18, 18, 24)) (xlabel, ylabel, titel)	
    Plottet die Datenreihe mit optionalen Fehlerbalken.    
    :return: None
    """

    if isinstance(data, list):
        x = data[0].copy()
        y = data[1].copy()

    # Überprüfen, ob obj2 ein NumPy-Array ist
    if isinstance(data, np.ndarray):
        x = data[:,0].copy()
        y = data[:,1].copy()

    plt.xlabel(xlabel, fontsize=label_sizes[0])
    plt.ylabel(ylabel, fontsize=label_sizes[1])
    plt.title(titel, fontsize=label_sizes[2],pad=20)
    plt.tick_params(axis='both', labelsize=18)
    plt.grid(grid)

    y_err = np.zeros_like(y)
    x_err = np.zeros_like(x)

    for i, d in enumerate(y):
        if isinstance(d, UFloat):
            y_err[i] = d.std_dev
            y[i] = d.nominal_value

    for i, d in enumerate(x):
        if isinstance(d, UFloat):
            x_err[i] = d.std_dev
            x[i] = d.nominal_value


    if interpolation == "linear":
        if error:

            if(y_err is [0] * len(y)):
                try:
                    if isinstance(data, list):
                        y_err = data[3]
                    elif isinstance(data, np.ndarray):
                        y_err = data[:,3]
                except Exception:
                    y_err = [0] * len(y)

            if x_err is [0] * len(x):
                try:
                    if isinstance(data, list):
                        x_err = data[2]            
                    elif isinstance(data, np.ndarray):
                        x_err = data[:,2]
                except Exception:
                    x_err = [0] * len(x)

            plt.errorbar(x, y, yerr=y_err, xerr=x_err, fmt=fmtp, 
                         label=label, capsize=5,ecolor="red",
                         markersize=markersize,linewidth=linewidth,
                         markeredgewidth=markerwidth,
                         elinewidth=1,
                         capthick = 1,
                         color = color_line)
        else:
            plt.plot(x, y, fmtp, 
                     label=label, 
                     markersize=markersize, 
                     linewidth=linewidth,
                     markeredgewidth=markerwidth,
                     color = color_line)
    else:
        f = sci.interp1d(x, y, kind=interpolation)
        x_int = np.linspace(x[0], x[-1], 1000, True)
        y_int = f(x_int)
        plt.plot(x_int, y_int, fmtp, label=label, linewidth=linewidth,
                 color = color_line)
        
    if label is not None:
        plt.legend(loc = leg_loc,fontsize=18)

def Mehrere_Datenreihen_ein_Plot(data_list, titel="", xlabel="x-Achse", 
                             ylabel="y-Achse", fmtp='-', error = False,
                             grid=False, labels=None, 
                             interpolation_list="linear", leg_loc="best",
                             label_sizes=(24,24,30),linewidths=2, markersizes = 10, 
                             markerwiths = 2, colors = None):
    """
    Plotte mehrere Datenreihen.
    param data_list: Liste von Arrays mit den Daten
        Jedes Array enthält:
        1) x-Werte,
        2) y-Werte,
        3) Fehler in y-Richtung (optional)
        4) Fehler in x-Richtung (optional)
    :param titel: Titel des Plots
    :param xlabel: Beschriftung der x-Achse
    :param ylabel: Beschriftung der y-Achse
    :param fmtp: Formatierungsparameter für die Plots
    :param error: Ob Fehlerbalken gezeichnet werden sollen
    :param legend: Ob eine Legende angezeigt werden soll
    :param grid: Ob ein Gitter angezeigt werden soll
    :param labels: Liste von Labels für die Legende (optional)
    :param fmt_punkte: Formatierungsparameter für die Punkte (optional)
    :param interpolation: Art der Interpolation (optional, Standard: "linear", "cubic", "nearest", "quadratic")
    :param leg_loc: Position der Legende (optional, Standard: "upper right")
    :param label_sizes: Größen der Labels (optional, Standard: (18, 18, 24)) (xlabel, ylabel, titel)
    Plottet die Datenreihen mit optionalen Fehlerbalken.
    :return: None
    """    
    
    if not isinstance(interpolation_list, list):
        interpolation_list = [interpolation_list] * len(data_list)
    if not isinstance(fmtp, list):
        fmtp = [fmtp] * len(data_list)
    if not isinstance(error, list):
        error = [error] * len(data_list)
    if not isinstance(linewidths, list):
        linewidths = [linewidths] * len(data_list)
    if not isinstance(markersizes, list):
        markersizes = [markersizes] * len(data_list)
    if not isinstance(markerwiths, list):
        markerwiths = [markerwiths] * len(data_list)
    if not isinstance(colors, list):
        colors = [colors] * len(data_list)


    for i, data in enumerate(data_list):
        label = labels[i] if labels else None
        Plot_Datenreihe(data, titel=titel, xlabel=xlabel, ylabel=ylabel,
                        fmtp=fmtp[i], error=error[i], grid=grid,
                        label=label, 
                        interpolation=interpolation_list[i],
                        leg_loc=leg_loc,
                        label_sizes=label_sizes,
                        linewidth=linewidths[i],
                        markersize=markersizes[i],
                        markerwidth=markerwiths[i],
                        color_line= colors[i])

def _erzeuge_subplot_layout(anz_plots, sharey=False, figsize=None):
    """
    Erzeugt die Figure und die Achsen für anz_plots Subplots.
    Es werden maximal 2 Plots pro Zeile gesetzt. Hat die letzte Zeile nur
    einen Plot (z. B. bei 3 Plots), wird dieser mittig platziert.

        1 Plot :  [   1   ]
        2 Plots:  [1] [2]
        3 Plots:  [1] [2]
                    [3]
        4 Plots:  [1] [2]
                  [3] [4]

    :return: fig, Liste der Achsen (in Plot-Reihenfolge)
    """
    ncols = 1 if anz_plots == 1 else 2
    nrows = math.ceil(anz_plots / ncols)

    if figsize is None:
        figsize = {1: (8, 6), 2: (8, 12)}.get(anz_plots, (16, 12))

    fig = plt.figure(figsize=figsize)
    # Doppelte Spaltenzahl, damit ein einzelner Plot mittig stehen kann
    gs = fig.add_gridspec(nrows, 2 * ncols)

    axes = []
    for i in range(anz_plots):
        row, col = divmod(i, ncols)
        alleine_in_letzter_zeile = (ncols == 2 and row == nrows - 1
                                    and anz_plots % 2 == 1)
        if alleine_in_letzter_zeile:
            spec = gs[row, 1:3]               # mittig
        else:
            spec = gs[row, 2 * col: 2 * col + 2]

        ax = fig.add_subplot(spec, sharey=axes[0] if (sharey and axes) else None)
        # Bei gemeinsamer y-Achse: Tick-Beschriftung nur links anzeigen
        if sharey and col > 0 and not alleine_in_letzter_zeile:
            ax.tick_params(labelleft=False)
        axes.append(ax)

    return fig, axes

def Mehrere_Datenreihen_verschiedene_Plots(
    data_list_p1, data_list_p2=None, data_list_p3=None,
    data_list_p4=None, titel_list=None, xlabel_list=None,
    ylabel_list=None, fmtp_list=None, error_list=None,
    grid_list=None, labels_list=None,
    interpolation_listen=None, leg_loc_list = "best",
    label_sizes_list=(24,24,30), linewidths_list=2, 
    sharey = False, markersize_list = 5 , markerwith_list = 1,
    colors_list = None, figsize = None):
    """
    Plotte mehrere Datenreihen in verschiedenen Subplots (max. 4).
    Jeder Datenblock (data_list_pn) enthält mehrere Kurven für einen Subplot.

    :param data_list_p1-4: Daten für bis zu 4 Subplots (Listen von Datenreihen)
    :param titel_list: Liste von Titeln für die einzelnen Plots
    :param xlabel_list: Liste der x-Achsen-Beschriftungen
    :param ylabel_list: Liste der y-Achsen-Beschriftungen
    :param fmtp_list: Liste von Formatstrings für die Kurven
    :param error_list: Liste von Booleans für Fehlerbalken
    :param legend_list: Liste von Booleans für Legenden
    :param grid_list: Liste von Booleans für Gitter
    :param labels_list: Liste von Listen für Legendenbeschriftungen
    :param fmt_punkte_listen: Liste von Formatstrings für die Punkte
    :param interpolation_listen: Liste von Interpolationsarten für die Kurven
    :param leg_loc_list: Liste von Positionen für die Legende
    :param label_sizes_list: Liste von Größen für die Achsenbeschriftungen (x, y, Titel)
    :return: None
    """

    Plots_data = [data_list_p1, data_list_p2, data_list_p3, data_list_p4]
    anz_plots = sum(p is not None for p in Plots_data)

    if anz_plots == 0:
        raise ValueError("Es muss mindestens eine Datenreihe angegeben werden.")
    if anz_plots > 4:
        raise ValueError("Maximal 4 Plots werden unterstützt.")
    # Standardwerte für Einzellisten setzen
    def expand(val, default, n):
        if isinstance(val, list):
            return val
        return [val if val is not None else default] * n

    titel_list   = expand(titel_list,   " ", anz_plots)
    xlabel_list  = expand(xlabel_list,  " ", anz_plots)
    ylabel_list  = expand(ylabel_list,  " ", anz_plots)
    fmtp_list    = expand(fmtp_list,    "-k", anz_plots)
    error_list   = expand(error_list,   False, anz_plots)
    grid_list    = expand(grid_list,    False, anz_plots)
    labels_list  = expand(labels_list,  None, anz_plots)
    colors_list  = expand(colors_list,  None, anz_plots)
    interpolation_listen = expand(interpolation_listen, "linear", anz_plots)
    leg_loc_list = expand(leg_loc_list, "upper right", anz_plots)
    label_sizes_list = expand(label_sizes_list, (18, 18, 24), anz_plots)
    linewidths_list = expand(linewidths_list, 2, anz_plots)
    markersize_list = expand(markersize_list, 2, anz_plots)
    markerwith_list = expand(markerwith_list, 2, anz_plots)
    # Figure und Achsen anlegen (3 Plots: 2 oben, 1 mittig darunter)
    fig, axes = _erzeuge_subplot_layout(anz_plots, sharey=sharey, figsize=figsize)

    plot_index = 0
    for i, data in enumerate(Plots_data):
        if data is None:
            continue

        # Passenden Subplot aktivieren
        plt.sca(axes[plot_index])

        # Plot zeichnen (deine bestehende Funktion wird verwendet!)
        Mehrere_Datenreihen_ein_Plot(
            data_list=data,
            titel=titel_list[plot_index],
            xlabel=xlabel_list[plot_index],
            ylabel=ylabel_list[plot_index],
            fmtp=fmtp_list[plot_index],
            error=error_list[plot_index],
            grid=grid_list[plot_index],
            labels=labels_list[plot_index],
            interpolation_list=interpolation_listen[plot_index],
            leg_loc=leg_loc_list[plot_index],
            label_sizes=label_sizes_list[plot_index],
            linewidths=linewidths_list[plot_index],
            markersizes=markersize_list[plot_index],
            markerwiths= markerwith_list[plot_index],
            colors= colors_list[plot_index]
        )

        plot_index += 1

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.3, bottom= 0.1, top=0.95)
    
def lineare_Regression(data):
    """
    Berechnet die lineare Regression für gegebene Daten.
    :param data: Array mit den Daten
        Erster Eintrag: x-Werte,
        Zweiter Eintrag: y-Werte,
        Dritter Eintrag: Fehler in y-Richtung (optional)
        Vierter Eintrag: Fehler in x-Richtung (optional)
    :return: Steigung, Achsenabschnitt, 
            mit einer Standardabweichung von 1 Sigma
            Steigungsfehler, Achsenabschnittsfehler
    """

    if isinstance(data, list):
        x = data[0]
        y = data[1]
    elif isinstance(data, np.ndarray):
        x = data[:, 0]
        y = data[:, 1]

    x = Ufloat_to_array(x)
    y = Ufloat_to_array(y)

    fit_parameter, cov_matrix = np.polyfit(x, y, 1, cov=True)
    steigung, ordinatenabstand = fit_parameter
    try:
        delta_steigung, delta_ordinatenabstand = np.sqrt(np.diag(cov_matrix))
    except Exception:
        delta_steigung, delta_ordinatenabstand = (None, None)

    t = np.linspace(np.min(x), np.max(x), 1000)
    y_fit = [t,steigung * t + ordinatenabstand]

    steigung = ufloat(steigung, delta_steigung)
    ordinatenabstand = ufloat(ordinatenabstand, delta_ordinatenabstand)

    return steigung, ordinatenabstand, y_fit

def fit_funktion(func, data, p0=None):
    """
    Fittet eine Funktion an die Daten.
    :param func: Funktion, die gefittet werden soll
    :param data: Array mit den Daten
        Erster Eintrag: x-Werte,
        Zweiter Eintrag: y-Werte,
        Dritter Eintrag: Fehler in y-Richtung (optional)
        Vierter Eintrag: Fehler in x-Richtung (optional)
    :param p0: Startwerte für die Parameter der Funktion (optional)
    :return: Optimierte Parameter und Fehler der Parameter
    """
    if isinstance(data, list):
        x = data[0]
        y = data[1]
    elif isinstance(data, np.ndarray):
        x = data[:, 0]
        y = data[:, 1]

    x = Ufloat_to_array(x)
    y = Ufloat_to_array(y)
    
    popt, pcov = opt.curve_fit(func, x, y, p0=p0)
    
    perr = np.sqrt(np.diag(pcov))
    parameter = csv_data_plus_error(popt,perr)
    
    return parameter