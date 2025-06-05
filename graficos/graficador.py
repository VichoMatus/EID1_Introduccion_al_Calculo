import numpy as np
import matplotlib.pyplot as plt

def graficar_elipses_2d(lista_elipses, titulo="Trayectorias del Dron"):
    fig, ax = plt.subplots(figsize=(5, 5))
    for i, (h, k, a, b) in enumerate(lista_elipses):
        theta = np.linspace(0, 2 * np.pi, 300)
        x = h + a * np.cos(theta)
        y = k + b * np.sin(theta)
        ax.plot(x, y, label=f"Elipse {i+1}")
        ax.plot(h, k, 'ro')  # Centro
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
