import numpy as np

def Bisektionsverfahren(f, a, b, tol=1e-6, max_iter=100):
    """
    Findet eine Nullstelle der Funktion f im Intervall [a, b] mittels des Bisektionsverfahrens.
    
    Parameter:
    f : Funktion, deren Nullstelle gefunden werden soll
    a : linke Grenze des Intervalls
    b : rechte Grenze des Intervalls
    tol : Toleranz für die Genauigkeit der Nullstelle
    max_iter : maximale Anzahl an Iterationen
    
    Rückgabe:
    x_mid : gefundene Nullstelle
    """
    Schritte = []
    
    if f(a) * f(b) >= 0:
        return np.nan, []
    
    for i in range(max_iter):
        x_mid = (a + b) / 2

        Schritte.append([x_mid])

        if abs(f(x_mid)) < tol and (b - a) / 2 < tol:
            return x_mid, np.array(Schritte)
        
        if f(x_mid) * f(a) < 0:
            b = x_mid
        else:
            a = x_mid
            
    raise ValueError("Maximale Anzahl an Iterationen erreicht. Keine Nullstelle gefunden.")

def Newtonverfahren(f, df, x0, tol=1e-6, max_iter=100):
    """
    Findet eine Nullstelle der Funktion f mittels des Newton-Verfahrens.
    
    Parameter:
    f : Funktion, deren Nullstelle gefunden werden soll
    df : Ableitung der Funktion f
    x0 : Startwert für die Iteration
    tol : Toleranz für die Genauigkeit der Nullstelle
    max_iter : maximale Anzahl an Iterationen
    
    Rückgabe:
    x : gefundene Nullstelle
    """
    Schritte = []
    
    x = x0
    for i in range(max_iter):
        Schritte.append([x])

        # Sobalt df(x) = 0 wird geht das nicht mehr
        # => Anderen Statpunkt wählen

        x_new = x - f(x) / df(x)
        
        if abs(f(x_new)) < tol and abs(x_new - x) < tol:
            return x_new, np.array(Schritte)
        
        x = x_new
        
    raise ValueError("Maximale Anzahl an Iterationen erreicht. Keine Nullstelle gefunden.")

def Zeros_in_Area(f, a, b, epsilon=1e-4):
    """Nullstellen von f in [a, b]: Vorzeichenwechsel auf Gitter suchen, dann Bisektion."""
    
    n = int(round(abs(b - a) / epsilon))            # Berechnen der Schritte
    xs = np.linspace(a, b, n + 1)                   # x-Werte für auswertung
    fs = f(xs)                                      # ein einziger Aufruf
    idx = np.nonzero(fs[:-1] * fs[1:] < 0)[0]       # Intervalle mit Vorzeichenwechsel
    return np.array([Bisektionsverfahren(f, xs[i], xs[i + 1])[0] for i in idx])

