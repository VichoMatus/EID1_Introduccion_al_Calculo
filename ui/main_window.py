import customtkinter as ctk
from logic.calculos import separar_rut, funcion_caso1, funcion_caso2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graficos.graficador import graficar_elipses_2d, graficar_elipses_3d
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

        # Contenedor principal para 2 columnas
        self.main_formula_frame = ctk.CTkFrame(self.tabview.tab("Datos y Formula"))
        self.main_formula_frame.pack(pady=10, fill="both", expand=True)

        # Frame izquierdo
        self.formula_frame_izq = ctk.CTkFrame(self.main_formula_frame)
        self.formula_frame_izq.pack(side="left", fill="both", expand=True, padx=10)

        self._crear_formulario(self.formula_frame_izq, lado="izq")

        # Frame derecho
        self.formula_frame_der = ctk.CTkFrame(self.main_formula_frame)
        self.formula_frame_der.pack(side="right", fill="both", expand=True, padx=10)

        self.parametros_izq = None
        self.parametros_der = None

        self._crear_formulario(self.formula_frame_der, lado="der")

        # Gráficos
        self.grafico_2d_btn = ctk.CTkButton(self.tabview.tab("Gráficos"), text="Ver gráfico en 2D", command=self.graficar)
        self.grafico_2d_btn.pack(pady=10)

        self.grafico_3d_btn = ctk.CTkButton(self.tabview.tab("Gráficos"), text="Ver gráfico en 3D", command=self.graficar_3d)
        self.grafico_3d_btn.pack(pady=10)

        self.grafico_frame = ctk.CTkFrame(self.tabview.tab("Gráficos"))
        self.grafico_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.h = self.k = self.a = self.b = 0

    def _crear_formulario(self, parent, lado):
        setattr(self, f"rut_entry_{lado}", ctk.CTkEntry(parent))
        getattr(self, f"rut_entry_{lado}").pack(pady=5)

        btn = ctk.CTkButton(parent, text="Guardar RUT", command=lambda l=lado: self._procesar_rut(l))
        btn.pack(pady=5)

        setattr(self, f"titulo_label_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=16, weight="bold")))
        getattr(self, f"titulo_label_{lado}").pack()

        setattr(self, f"valor_label_{lado}", ctk.CTkLabel(parent, text=""))
        getattr(self, f"valor_label_{lado}").pack()

        setattr(self, f"orientacion_label_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14, weight="bold")))
        getattr(self, f"orientacion_label_{lado}").pack(pady=5)

        # Título para ecuación canónica
        setattr(self, f"canonica_titulo_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14, weight="bold")))
        getattr(self, f"canonica_titulo_{lado}").pack()

        setattr(self, f"formula_label_{lado}", ctk.CTkLabel(parent, text=""))
        getattr(self, f"formula_label_{lado}").pack()

        # Título para ecuación general
        setattr(self, f"general_titulo_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14, weight="bold")))
        getattr(self, f"general_titulo_{lado}").pack(pady=(10, 0))

        setattr(self, f"general_label_{lado}", ctk.CTkLabel(parent, text="", wraplength=400, justify="center"))
        getattr(self, f"general_label_{lado}").pack()

        setattr(self, f"valores_titulo_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=14, weight="bold")))
        getattr(self, f"valores_titulo_{lado}").pack()

        setattr(self, f"debug_label_{lado}", ctk.CTkLabel(parent, text="", font=ctk.CTkFont(size=12), justify="left"))
        getattr(self, f"debug_label_{lado}").pack(pady=10)


    def _procesar_rut(self, lado):
        rut_entry = getattr(self, f"rut_entry_{lado}")
        rut = rut_entry.get()
        rut_separado = separar_rut(rut)

        if len(rut_separado) < 8:
            for nombre in [
                "titulo", "valor", "formula", "orientacion", "general",
                "debug", "canonica_titulo", "general_titulo", "valores_titulo"
            ]:
                label = getattr(self, f"{nombre}_label_{lado}", None) or getattr(self, f"{nombre}_{lado}", None)
                if label:
                    label.configure(text="", image=None)
            return

        ultimo = rut_separado[-1]
        if ultimo.isdigit():
            resultado = funcion_caso2(rut_separado) if int(ultimo) % 2 == 0 else funcion_caso1(rut_separado)
            h, k, a, b = resultado["h"], resultado["k"], resultado["a"], resultado["b"]
            orientacion = resultado["orientacion"]
            canonica = render_formula(H=h, K=k, A=a, B=b)
            general = render_formula_general(resultado["latex_general"])

            self.h, self.k, self.a, self.b = h, k, a, b  # Para graficar
            if lado == "izq":
                self.parametros_izq = (h, k, a, b)
            else:
                self.parametros_der = (h, k, a, b)


            getattr(self, f"titulo_label_{lado}").configure(text="Ecuación Canónica con RUT:")
            getattr(self, f"valor_label_{lado}").configure(text=rut)
            getattr(self, f"orientacion_label_{lado}").configure(text=f"Orientación:\n{orientacion}")

            getattr(self, f"canonica_titulo_{lado}").configure(text="Ecuación Canónica:")
            getattr(self, f"formula_label_{lado}").configure(image=canonica)

            getattr(self, f"general_titulo_{lado}").configure(text="Ecuación General:")
            getattr(self, f"general_label_{lado}").configure(image=general, text="")

            setattr(self, f"foto_canonica_{lado}", canonica)
            setattr(self, f"foto_general_{lado}", general)

            # Mostrar explicación de valores h, k, a, b
            getattr(self, f"valores_titulo_{lado}").configure(text="Valores Ecuación Canónica:")

            explicacion = (
                f"h = d1 = {rut_separado[0]}\n"
                f"k = d2 = {rut_separado[1]}\n"
            )

            if int(ultimo) % 2 == 0:
                # Caso 2
                explicacion += (
                    f"a = d6 + d7 = {rut_separado[5]} + {rut_separado[6]} = {a}\n"
                    f"b = d8 + d3 = {rut_separado[7]} + {rut_separado[2]} = {b}"
                )
            else:
                # Caso 1
                explicacion += (
                    f"a = d3 + d4 = {rut_separado[2]} + {rut_separado[3]} = {a}\n"
                    f"b = d5 + d6 = {rut_separado[4]} + {rut_separado[5]} = {b}"
                )

            getattr(self, f"debug_label_{lado}").configure(text=explicacion)

    def mostrar_grafico(self, fig):
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()
        plt.close('all')
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def graficar(self):
        elipses = []
        if self.parametros_izq:
            elipses.append(self.parametros_izq)
        if self.parametros_der:
            elipses.append(self.parametros_der)

        if elipses:
            fig, ax = graficar_elipses_2d(elipses)
            self.mostrar_grafico(fig)


    def graficar_3d(self):
        elipses = []
        if self.parametros_izq:
            elipses.append(self.parametros_izq)
        if self.parametros_der:
            elipses.append(self.parametros_der)

        if elipses:
            fig, ax = graficar_elipses_3d(elipses)
            self.mostrar_grafico(fig)

