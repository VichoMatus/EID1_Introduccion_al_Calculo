def separar_rut(rut: str):
    # Quitar puntos y guion, y separar dígitos numéricos
    # Además, si termina en K o k, agregar '0' al final
    rut = rut.replace(".", "").replace("-", "")
    digitos = list(rut[:-1])  # Todos excepto el último carácter
    ultimo = rut[-1].upper()
    
    if ultimo == "K":
        digitos.append('0')
    else:
        digitos.append(ultimo)
    
    return digitos

def funcion_caso1(digitos):
    h = int(digitos[0])
    k = int(digitos[1])
    a = int(digitos[2]) + int(digitos[3])
    b = int(digitos[4]) + int(digitos[5])
    orientacion = "horizontal" if int(digitos[7]) % 2 == 0 else "vertical"

    A = 1 / (a ** 2)
    B = 1 / (b ** 2)
    D = -2 * h * A
    E = -2 * k * B
    F = A * h ** 2 + B * k ** 2 - 1

    return {
        "h": h, "k": k, "a": a, "b": b, "orientacion": orientacion,
        "general": f"{A:.3f}x² + {B:.3f}y² + {D:.3f}x + {E:.3f}y + {F:.3f} = 0"
    }

def funcion_caso2(digitos):
    h = int(digitos[0])
    k = int(digitos[1])
    a = int(digitos[5]) + int(digitos[6])
    b = int(digitos[7]) + int(digitos[2])
    orientacion = "horizontal" if int(digitos[3]) % 2 == 0 else "vertical"

    A = 1 / (a ** 2)
    B = 1 / (b ** 2)
    D = -2 * h * A
    E = -2 * k * B
    F = A * h ** 2 + B * k ** 2 - 1

    return {
        "h": h, "k": k, "a": a, "b": b, "orientacion": orientacion,
        "general": f"{A:.3f}x² + {B:.3f}y² + {D:.3f}x + {E:.3f}y + {F:.3f} = 0"
    }