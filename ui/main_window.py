import customtkinter as ctk
import numpy as np
from logic.calculos import separar_rut, funcion_caso1, funcion_caso2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
import matplotlib.pyplot as plt
from graficos.graficador import graficar_elipse_2d, graficar_elipse_3d
from logic.render_formulas import render_formula, render_formula_general

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.geometry("1280x720")
        self.title("Ventana Principal")

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill="both")

        self.tabview.add("Datos y Formula")
        self.tabview.add("Gráficos")

        self.rut_label = ctk.CTkLabel(self.tabview.tab("Datos y Formula"), text="Ingrese RUT (con puntos y guion):")
        self.rut_label.pack(pady=10)

        self.rut_entry = ctk.CTkEntry(self.tabview.tab("Datos y Formula"))
        self.rut_entry.pack(pady=10)

        self.guardar_btn = ctk.CTkButton(self.tabview.tab("Datos y Formula"), text="Guardar RUT", command=self.guardar_rut)
        self.guardar_btn.pack(pady=10)

        self.formula_frame = ctk.CTkFrame(self.tabview.tab("Datos y Formula"), height=300)
        self.formula_frame.pack(pady=10, fill="both", expand=False)

        self.rut_label_formula = ctk.CTkLabel(self.formula_frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.rut_label_formula.pack(pady=(0,5), anchor="center")

        self.rut_valor_label = ctk.CTkLabel(self.formula_frame, text="", font=ctk.CTkFont(size=14))
        self.rut_valor_label.pack(pady=(5,10), anchor="center")

        self.formula_label = ctk.CTkLabel(self.formula_frame, text="")
        self.formula_label.pack(anchor="center")

        self.orientacion_label = ctk.CTkLabel(self.formula_frame, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color="black")
        self.orientacion_label.pack(pady= (10,10), anchor="center")

        self.general_label = ctk.CTkLabel(self.formula_frame, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="black", wraplength=500, justify="center")
        self.general_label.pack(pady=(20,10), anchor="center")

        self.grafico_2d_btn = ctk.CTkButton(self.tabview.tab("Gráficos"), text="Ver gráfico en 2D", command=self.graficar)
        self.grafico_2d_btn.pack(pady=10)

        self.grafico_3d_btn = ctk.CTkButton(self.tabview.tab("Gráficos"), text="Ver gráfico en 3D", command=self.graficar_3d)
        self.grafico_3d_btn.pack(pady=10)

        self.grafico_frame = ctk.CTkFrame(self.tabview.tab("Gráficos"))
        self.grafico_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.rut_separado = []
        self.formula_photo = None


    def guardar_rut(self):
        rut = self.rut_entry.get()
        self.rut_separado = separar_rut(rut)

        if len(self.rut_separado) < 8:
            self.rut_label_formula.configure(text="")
            self.rut_valor_label.configure(text="")
            self.formula_label.configure(image=None)
            self.orientacion_label.configure(text="")
            self.general_label.configure(image=None, text="")
            return

        ultimo_digito = self.rut_separado[-1]
        if ultimo_digito.isdigit():
            ultimo_num = int(ultimo_digito)

            if ultimo_num == 0 or ultimo_num % 2 == 0:
                resultado = funcion_caso2(self.rut_separado)
            else:
                resultado = funcion_caso1(self.rut_separado)

            self.h = resultado["h"]
            self.k = resultado["k"]
            self.a = resultado["a"]
            self.b = resultado["b"]
            orientacion = resultado["orientacion"]
            formula_general = resultado["latex_general"]

            self.rut_label_formula.configure(text="Ecuación Canónica con RUT:")
            self.rut_valor_label.configure(text=rut)

            self.formula_photo = render_formula(
                X='x', Y='y', H=self.h, K=self.k, A=str(self.a), B=str(self.b)
            )
            self.formula_label.configure(image=self.formula_photo)

            self.orientacion_label.configure(text=f"Orientación:\n {orientacion}")

            # Renderizar fórmula general en LaTeX como imagen
            self.general_photo = render_formula_general(formula_general)
            self.general_label.configure(image=self.general_photo, text="")


        else:
            self.rut_label_formula.configure(text="")
            self.rut_valor_label.configure(text="")
            self.formula_label.configure(image=None)
            self.orientacion_label.configure(text="")
            self.general_label.configure(image=None, text="")


    def mostrar_grafico(self, fig):
        # Limpia el frame y cierra figuras previas para liberar recursos
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        plt.close('all')  # Asegura cerrar figuras anteriores
        
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def graficar(self):
        fig, ax = graficar_elipse_2d(self.h, self.k, self.a, self.b)
        self.mostrar_grafico(fig)

    def graficar_3d(self):
        fig, ax = graficar_elipse_3d(self.h, self.k, self.a, self.b)
        self.mostrar_grafico(fig)
