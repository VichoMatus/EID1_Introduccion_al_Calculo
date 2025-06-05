import numpy as np
import matplotlib.pyplot as plt

def graficar_elipse_2d(h, k, a, b, titulo="Trayectoria del Dron"):
    theta = np.linspace(0, 2 * np.pi, 300)
    x = h + a * np.cos(theta)
    y = k + b * np.sin(theta)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x, y, label="Elipse")
    ax.plot(h, k, 'ro', label="Centro")
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True)
    return fig, ax

def graficar_elipse_3d(h, k, a, b, titulo="Trayectoria 3D del Dron"):
    theta = np.linspace(0, 2 * np.pi, 300)
    x = h + a * np.cos(theta)
    y = k + b * np.sin(theta)
    z = np.zeros_like(theta)

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label="Elipse en plano XY")
    ax.scatter([h], [k], [0], color='red', label="Centro")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title(titulo)
    ax.legend()
    plt.tight_layout()
    return fig, ax
