import customtkinter as ctk
import numpy as np
from logic.calculos import separar_rut, funcion_caso1, funcion_caso2
import matplotlib
#matplotlib.use('Agg')  # Backend no interactivo para matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import io

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.geometry("1280x720")
        self.title("Ventana Principal")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        # Agregar las pestañas
        self.tabview.add("Datos y Formula")
        self.tabview.add("Gráficos")  # Pestaña nueva agregada

        # Widgets pestaña Datos y Formula
        self.rut_label = ctk.CTkLabel(self.tabview.tab("Datos y Formula"), text="Ingrese RUT (con puntos y guion):")
        self.rut_label.pack(pady=10)

        self.rut_entry = ctk.CTkEntry(self.tabview.tab("Datos y Formula"))
        self.rut_entry.pack(pady=10)

        self.guardar_btn = ctk.CTkButton(self.tabview.tab("Datos y Formula"), text="Guardar RUT", command=self.guardar_rut)
        self.guardar_btn.pack(pady=10)

        # Frame para mostrar fórmula en Datos y Formula
        self.formula_frame = ctk.CTkFrame(self.tabview.tab("Datos y Formula"), height=300)
        self.formula_frame.pack(pady=10, fill="both", expand=False)

        self.rut_label_formula = ctk.CTkLabel(
            self.formula_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.rut_label_formula.pack(pady=(0,5), anchor="center")

        self.rut_valor_label = ctk.CTkLabel(
            self.formula_frame,
            text="",
            font=ctk.CTkFont(size=14)
        )
        self.rut_valor_label.pack(pady=(5,10), anchor="center")

        self.formula_label = ctk.CTkLabel(self.formula_frame, text="")
        self.formula_label.pack(anchor="center")

        self.orientacion_label = ctk.CTkLabel(
            self.formula_frame,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="black"
        )
        self.orientacion_label.pack(pady= (10,10), anchor="center")

        self.general_label = ctk.CTkLabel(
            self.formula_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="black",
            wraplength=500,  # Para que no se salga del cuadro
            justify="center"
        )
        self.general_label.pack(pady=(20,10), anchor="center")

        
        self.grafico_2d_btn = ctk.CTkButton(self.tabview.tab("Gráficos"), text="Ver grafico en 2D", command=self.graficar)
        self.grafico_2d_btn.pack(pady=10)

        # self.grafico_3d_btn = ctk.CTkLabel(self.tabview.tab("Gráficos"), text="Ver grafico en 3D", command=lambda: print("Función 3D no implementada"))
        #self.grafico_3d_btn.pack(pady=20)

        # Pestaña gráficos 
        self.grafico_frame = ctk.CTkFrame(self.tabview.tab("Gráficos"))
        self.grafico_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.rut_separado = []
        self.formula_photo = None  # Para mantener referencia a la imagen

    def render_formula(self, X='x', Y='y', H='h', K='k', A='a', B='b'):
        plt.clf()
        fig = plt.figure(figsize=(6, 2), dpi=100)
        plt.axis('off')

        formula = rf"\frac{{({X} - {H})^2}}{{{A}^2}} + \frac{{({Y} - {K})^2}}{{{B}^2}} = 1"
        plt.text(0.5, 0.5, f"${formula}$", fontsize=20, ha='center', va='center')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
        buf.seek(0)
        plt.close(fig)
        img = Image.open(buf)
        return ImageTk.PhotoImage(img)

    def guardar_rut(self):
        rut = self.rut_entry.get()
        self.rut_separado = separar_rut(rut)

        if len(self.rut_separado) < 8:
            self.rut_label_formula.configure(text="")
            self.rut_valor_label.configure(text="")
            self.formula_label.configure(image=None)
            self.orientacion_label.configure(text="")
            self.general_label.configure(text="")
            return

        ultimo_digito = self.rut_separado[-1]
        if ultimo_digito.isdigit():
            ultimo_num = int(ultimo_digito)

            if ultimo_num == 0 or ultimo_num % 2 == 0:  # Caso par
                resultado = funcion_caso2(self.rut_separado)
            else:  # Caso impar
                resultado = funcion_caso1(self.rut_separado)

            self.h = resultado["h"]
            self.k = resultado["k"]
            self.a = resultado["a"]
            self.b = resultado["b"]
            orientacion = resultado["orientacion"]
            formula_general = resultado["general"]

            self.rut_label_formula.configure(text="Ecuación Canónica con RUT:")
            self.rut_valor_label.configure(text=rut)

            self.formula_photo = self.render_formula(X='x', Y='y', H=self.h, K=self.k, A=str(self.a), B=str(self.b))
            self.formula_label.configure(image=self.formula_photo)

            self.orientacion_label.configure(text=f"Orientación:\n {orientacion}")
            self.general_label.configure(text=f"Ecuación general:\n {formula_general}") 


        else:
            self.rut_label_formula.configure(text="")
            self.rut_valor_label.configure(text="")
            self.formula_label.configure(image=None)
            self.orientacion_label.configure(text="")
            self.general_label.configure(text="")

    def graficar_elipse(self, h, k, a, b):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        theta = np.linspace(0, 2 * np.pi, 300)
        x = h + a * np.cos(theta)
        y = k + b * np.sin(theta)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.plot(x, y, label="Elipse")
        ax.plot(h, k, 'ro', label="Centro")
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Trayectoria del Dron")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def graficar(self):
        self.graficar_elipse(self.h, self.k, self.a, self.b)
