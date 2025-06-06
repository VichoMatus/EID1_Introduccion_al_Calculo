def separar_rut(rut: str):
    # Quitar puntos y guion, y separar dígitos numéricos
    rut = rut.replace(".", "").replace("-", "")
    digitos = list(rut[:-1])  # Todos excepto el último carácter
    ultimo = rut[-1].upper()

    if ultimo == "K":
        digitos.append('0')
    else:
        digitos.append(ultimo)

    return digitos

#caso digito verificador impar
def funcion_caso1(digitos):
    h = int(digitos[0])
    k = int(digitos[1])
    a = int(digitos[2]) + int(digitos[3])
    b = int(digitos[4]) + int(digitos[5])
    orientacion = "horizontal" if int(digitos[7]) % 2 == 0 else "vertical"

    if orientacion == "horizontal":
        if a < b:
            a, b = b, a
        A = 1 / (a ** 2)
        B = 1 / (b ** 2)
        canonica = f"\\frac{{(x - {h})^2}}{{{a}^2}} + \\frac{{(y - {k})^2}}{{{b}^2}} = 1"
    else:
        if b < a:
            a, b = b, a
        A = 1 / (b ** 2)
        B = 1 / (a ** 2)
        canonica = f"\\frac{{(x - {h})^2}}{{{b}^2}} + \\frac{{(y - {k})^2}}{{{a}^2}} = 1"

    D = -2 * h * A
    E = -2 * k * B
    F = A * h ** 2 + B * k ** 2 - 1

    latex_general = (
        f"{A:.3f}x^2 {'+' if B >= 0 else '-'} {abs(B):.3f}y^2 "
        f"{'+' if D >= 0 else '-'} {abs(D):.3f}x "
        f"{'+' if E >= 0 else '-'} {abs(E):.3f}y "
        f"{'+' if F >= 0 else '-'} {abs(F):.3f} = 0"
    )

    return {
        "h": h, "k": k, "a": a, "b": b, "orientacion": orientacion,
        "canonica": canonica,
        "latex_general": latex_general
    }

#caso digito verificador par
def funcion_caso2(digitos):
    h = int(digitos[0])
    k = int(digitos[1])
    a = int(digitos[5]) + int(digitos[6])
    b = int(digitos[7]) + int(digitos[2])
    orientacion = "horizontal" if int(digitos[3]) % 2 == 0 else "vertical"

    if orientacion == "horizontal":
        if a < b:
            a, b = b, a
        A = 1 / (a ** 2)
        B = 1 / (b ** 2)
        canonica = f"\\frac{{(x - {h})^2}}{{{a}^2}} + \\frac{{(y - {k})^2}}{{{b}^2}} = 1"
    else:
        if b < a:
            a, b = b, a
        A = 1 / (b ** 2)
        B = 1 / (a ** 2)
        canonica = f"\\frac{{(x - {h})^2}}{{{b}^2}} + \\frac{{(y - {k})^2}}{{{a}^2}} = 1"

    D = -2 * h * A
    E = -2 * k * B
    F = A * h ** 2 + B * k ** 2 - 1

    latex_general = (
        f"{A:.3f}x^2 {'+' if B >= 0 else '-'} {abs(B):.3f}y^2 "
        f"{'+' if D >= 0 else '-'} {abs(D):.3f}x "
        f"{'+' if E >= 0 else '-'} {abs(E):.3f}y "
        f"{'+' if F >= 0 else '-'} {abs(F):.3f} = 0"
    )

    return {
        "h": h, "k": k, "a": a, "b": b, "orientacion": orientacion,
        "canonica": canonica,
        "latex_general": latex_general
    }