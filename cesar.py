#!/usr/bin/env python3
"""
cesar.py - Cifrado Cesar

Uso:
    python3 cesar.py "<string a cifrar>" <desplazamiento>

Ejemplo:
    python3 cesar.py "criptografia y seguridad en redes" 9
"""

import sys


def cifrar_cesar(texto: str, desplazamiento: int) -> str:
    resultado = []
    for caracter in texto:
        if caracter.isalpha():
            base = ord('A') if caracter.isupper() else ord('a')
            nuevo = (ord(caracter) - base + desplazamiento) % 26 + base
            resultado.append(chr(nuevo))
        else:
            # Espacios, numeros y simbolos se dejan sin modificar
            resultado.append(caracter)
    return "".join(resultado)


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 cesar.py \"<string a cifrar>\" <desplazamiento>")
        sys.exit(1)

    texto = sys.argv[1]

    try:
        desplazamiento = int(sys.argv[2])
    except ValueError:
        print("Error: el desplazamiento debe ser un numero entero.")
        sys.exit(1)

    texto_cifrado = cifrar_cesar(texto, desplazamiento)
    print(texto_cifrado)


if __name__ == "__main__":
    main()
