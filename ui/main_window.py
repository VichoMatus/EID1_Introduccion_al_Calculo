import customtkinter as ctk
from logic.calculos import separar_rut, funcion_caso1, funcion_caso2
import matplotlib
matplotlib.use('Agg')  # Backend no interactivo para matplotlib
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
            font=ctk.CTkFont(size=14, slant="italic"),
            text_color="black"
        )
        self.orientacion_label.pack(anchor="center")

        # Pestaña gráficos (vacía por ahora)
        self.graficos_label = ctk.CTkLabel(self.tabview.tab("Gráficos"), text="Aquí irán los gráficos")
        self.graficos_label.pack(pady=20)

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
            return

        ultimo_digito = self.rut_separado[-1]
        if ultimo_digito.isdigit():
            ultimo_num = int(ultimo_digito)

            if ultimo_num == 0 or ultimo_num % 2 == 0:  # Caso par
                h = self.rut_separado[0]
                k = self.rut_separado[1]
                a = int(self.rut_separado[5]) + int(self.rut_separado[6])
                b = int(self.rut_separado[7]) + int(self.rut_separado[2])
                orientacion = "horizontal" if int(self.rut_separado[3]) % 2 == 0 else "vertical"
                resultado = funcion_caso2(self.rut_separado)
            else:  # Caso impar
                h = self.rut_separado[0]
                k = self.rut_separado[1]
                a = int(self.rut_separado[2]) + int(self.rut_separado[3])
                b = int(self.rut_separado[4]) + int(self.rut_separado[5])
                orientacion = "horizontal" if int(self.rut_separado[7]) % 2 == 0 else "vertical"
                resultado = funcion_caso1(self.rut_separado)

            self.rut_label_formula.configure(text="Ecuacion Canonica con rut:")
            self.rut_valor_label.configure(text=rut)

            self.formula_photo = self.render_formula(X='x', Y='y', H=h, K=k, A=str(a), B=str(b))
            self.formula_label.configure(image=self.formula_photo)

            self.orientacion_label.configure(text=f"Orientación: {orientacion}", text_color="black", font=ctk.CTkFont(size=14, slant="italic"))

        else:
            self.rut_label_formula.configure(text="")
            self.rut_valor_label.configure(text="")
            self.formula_label.configure(image=None)
            self.orientacion_label.configure(text="")

