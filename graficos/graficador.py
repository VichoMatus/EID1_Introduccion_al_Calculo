import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def interseccion_elipses(elipse1, elipse2, tolerance=1e-4):
    """
    Calcula los puntos de intersección entre dos elipses dadas por sus parámetros.
    Elipses definidas como (h, k, a, b) donde (h, k) es el centro, y a, b son los semi-ejes.
    """
    h1, k1, a1, b1 = elipse1
    h2, k2, a2, b2 = elipse2

    # Definimos las ecuaciones paramétricas para cada elipse
    def ecuaciones(t):
        x1 = h1 + a1 * np.cos(t[0])
        y1 = k1 + b1 * np.sin(t[0])
        x2 = h2 + a2 * np.cos(t[1])
        y2 = k2 + b2 * np.sin(t[1])
        
        # Queremos que las coordenadas coincidan para encontrar la intersección
        return [x1 - x2, y1 - y2]
    
    # Usamos fsolve para encontrar las soluciones numéricas con más parámetros de control
    t_iniciales = [
        [0, 0], [np.pi / 4, np.pi / 4], [np.pi / 2, np.pi / 2], 
        [np.pi, np.pi], [3*np.pi/2, 3*np.pi/2], [np.pi/3, np.pi/3],
        [np.pi/6, np.pi/6], [5*np.pi/6, 5*np.pi/6], [2*np.pi, 2*np.pi],
        [-np.pi/4, -np.pi/4], [np.pi/5, np.pi/5]  # Más condiciones iniciales
    ]
    
    intersecciones = []
    for t_inicial in t_iniciales:
        t_solucion = fsolve(ecuaciones, t_inicial, xtol=1e-6, maxfev=5000)  # Aumento de las iteraciones máximas
        x_int = h1 + a1 * np.cos(t_solucion[0])
        y_int = k1 + b1 * np.sin(t_solucion[0])
        
        # Comprobamos si la intersección es válida, es decir, si las coordenadas son cercanas
        x_check = h2 + a2 * np.cos(t_solucion[1])
        y_check = k2 + b2 * np.sin(t_solucion[1])
        
        # Verificamos si la diferencia entre las coordenadas de ambas elipses es menor que la tolerancia
        if np.allclose([x_int, y_int], [x_check, y_check], atol=tolerance):
            intersecciones.append((x_int, y_int))
    
    # Eliminar duplicados si los puntos de intersección son muy cercanos
    intersecciones_unicas = []
    for punto in intersecciones:
        if not any(np.allclose(punto, otro_punto, atol=tolerance) for otro_punto in intersecciones_unicas):
            intersecciones_unicas.append(punto)

    return intersecciones_unicas

def graficar_elipses_2d(lista_elipses, titulo="Trayectorias del Dron"):
    fig, ax = plt.subplots(figsize=(5, 5))
    
    # Dibujar cada elipse
    for i, (h, k, a, b) in enumerate(lista_elipses):
        theta = np.linspace(0, 2 * np.pi, 300)
        x = h + a * np.cos(theta)
        y = k + b * np.sin(theta)
        ax.plot(x, y, label=f"Elipse {i+1}")
        ax.plot(h, k, 'ro')  # Centro de la elipse
        
        # Mostrar el centro de la elipse
        ax.text(h + 0.5, k + 0.5, f"Centro Elipse {i+1} ({h}, {k})", color='red', fontsize=8)

    # Buscar y graficar puntos de intersección entre todas las elipses
    puntos_interseccion = []
    for i in range(len(lista_elipses)):
        for j in range(i + 1, len(lista_elipses)):
            elipse1 = lista_elipses[i]
            elipse2 = lista_elipses[j]
            intersecciones = interseccion_elipses(elipse1, elipse2)
            for interseccion in intersecciones:
                puntos_interseccion.append(interseccion)
                # Graficar las intersecciones
                ax.plot(interseccion[0], interseccion[1], 'go')  # Puntos de intersección
                # Mostrar las coordenadas de la intersección en el gráfico
                ax.text(interseccion[0] + 0.3, interseccion[1] + 0.3, f'Intersección ({interseccion[0]:.2f}, {interseccion[1]:.2f})', 
                        color='green', fontsize=8)  # Mostrar las coordenadas
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True)
    return fig, ax


def graficar_elipses_3d(lista_elipses, titulo="Trayectorias 3D del Dron"):
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar cada elipse en 3D
    for i, (h, k, a, b) in enumerate(lista_elipses):
        theta = np.linspace(0, 2 * np.pi, 300)
        x = h + a * np.cos(theta)
        y = k + b * np.sin(theta)
        z = np.zeros_like(theta)
        ax.plot(x, y, z, label=f"Elipse {i+1}")
        ax.scatter([h], [k], [0], color='red')
    
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(titulo)
    ax.legend()
    plt.tight_layout()
    return fig, ax


def hay_interseccion(lista_elipses, tolerance=1e-4):
    """
    Retorna True si hay al menos un punto de intersección entre cualquier par de elipses en la lista.
    """
    if len(lista_elipses) < 2:
        return False
    for i in range(len(lista_elipses)):
        for j in range(i + 1, len(lista_elipses)):
            intersecciones = interseccion_elipses(lista_elipses[i], lista_elipses[j], tolerance)
            if intersecciones:
                return True
    return False
