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
    pass

def funcion_caso2(digitos):
    pass
