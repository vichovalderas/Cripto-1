#!/usr/bin/env python3
"""
readv2.py - Recuperación del mensaje cifrado desde captura .pcapng
Prueba los 26 posibles desplazamientos del cifrado César.
Uso académico: sudo python3 readv2.py cesar.pcapng
"""

import sys
from scapy.all import rdpcap, ICMP, Raw
from colorama import Fore, Style, init

# Inicializar colorama para colores en terminal
init(autoreset=True)

def descifrar_cesar(texto, desplazamiento):
    """Descifra un texto usando el algoritmo César con el desplazamiento indicado."""
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            base = ord('a') if caracter.islower() else ord('A')
            resultado += chr((ord(caracter) - base - desplazamiento) % 26 + base)
        else:
            resultado += caracter
    return resultado

def extraer_mensaje(pcap_file):
    """Extrae el payload de los paquetes ICMP Echo Request del archivo pcapng."""
    paquetes = rdpcap(pcap_file)
    mensaje = ""

    for paquete in paquetes:
        if paquete.haslayer(ICMP) and paquete[ICMP].type == 8:  # Echo Request
            if paquete.haslayer(Raw):
                payload = paquete[Raw].load
                # Tomamos solo el primer byte (un carácter)
                if payload:
                    try:
                        mensaje += payload[:1].decode('utf-8', errors='ignore')
                    except:
                        pass
    return mensaje

def es_probable(texto):
    """Heurística simple para detectar el mensaje más probable en español."""
    texto_lower = texto.lower()
    palabras_clave = ["criptografia", "seguridad", "redes", "criptografía"]
    return any(palabra in texto_lower for palabra in palabras_clave)

def main():
    if len(sys.argv) != 2:
        print(f"Uso: sudo python3 {sys.argv[0]} <archivo.pcapng>")
        sys.exit(1)

    archivo = sys.argv[1]
    print(f"[*] Leyendo captura: {archivo}")

    cifrado = extraer_mensaje(archivo)

    if not cifrado:
        print("No se encontró ningún payload ICMP válido.")
        sys.exit(1)

    print(f"[*] Mensaje cifrado reconstruido: {cifrado}\n")
    print("[*] Probando los 26 posibles desplazamientos:\n")

    for shift in range(26):
        claro = descifrar_cesar(cifrado, shift)

        if es_probable(claro):
            # Destacar en verde la opción más probable
            print(f"{Fore.GREEN}{shift:2d}  {claro}{Style.RESET_ALL}")
        else:
            print(f"{shift:2d}  {claro}")

if __name__ == "__main__":
    main()
