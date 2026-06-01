"""
sys_toolkit.py — Kit de herramientas para administradores de sistemas
Menú principal interactivo CLI que integra todos los módulos.
"""

import sys
from typing import NoReturn

# ── Importaciones de módulos del toolkit ──────────────────────────
from os_utils      import check_ping, check_disk_space
from log_parser    import parse_auth_log, count_failed_ips
from threat_intel  import show_threat_table
from inventory_manager import run_inventory_report
from network_models import Router, Server


def print_banner() -> None:
    """Imprime el banner de bienvenida."""
    print("\n" + "═" * 55)
    print("  🛡  SYS-TOOLKIT — Kit para Administradores de Red")
    print("═" * 55)


def print_menu() -> None:
    """Imprime el menú principal."""
    print("\n  MÓDULOS DISPONIBLES")
    print("  ─────────────────────────────────────────────────")
    print("  1. 📡  Comprobar conectividad (ping a una IP)")
    print("  2. 💾  Comprobar espacio en disco")
    print("  3. 🔍  Analizar logs de SSH (auth.log)")
    print("  4. 🌍  Geolocalizar IPs sospechosas")
    print("  5. 📊  Generar informe de inventario Excel")
    print("  6. 🖥  Demo de modelos de red (POO)")
    print("  0. 🚪  Salir")
    print("  ─────────────────────────────────────────────────")


def handle_ping() -> None:
    ip: str = input("  IP a comprobar: ").strip()
    if not ip:
        print("  ⚠ Introduce una IP válida.")
        return
    resultado: bool = check_ping(ip)
    estado = "✅ RESPONDE" if resultado else "❌ NO RESPONDE"
    print(f"  {ip} → {estado}")


def handle_disk() -> None:
    ruta: str = input("  Ruta de la partición [/ por defecto]: ").strip() or "/"
    check_disk_space(ruta)


def handle_logs() -> None:
    ruta: str = input("  Ruta del auth.log [data/auth.log]: ").strip() or "data/auth.log"
    try:
        failed_ips, successful_ips = parse_auth_log(ruta)
        counts = count_failed_ips(failed_ips)
        print(f"\n  IPs únicas con fallos: {len(counts)}")
        print(f"  Intentos exitosos:     {len(successful_ips)}")
        print("\n  TOP 10 IPs más agresivas:")
        print("  " + "─" * 35)
        for ip, n in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {ip:<20} {n:>4} intentos")
    except FileNotFoundError:
        print(f"  ⚠ No se encontró el archivo: {ruta}")
        print("  Genera primero el log de prueba con: python data/generate_sample_log.py")


def handle_threat() -> None:
    ruta: str = input("  Ruta del auth.log [data/auth.log]: ").strip() or "data/auth.log"
    try:
        failed_ips, _ = parse_auth_log(ruta)
        counts = count_failed_ips(failed_ips)
        top_ips = [ip for ip, _ in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]]
        show_threat_table(top_ips, counts)
    except FileNotFoundError:
        print(f"  ⚠ No se encontró: {ruta}")


def handle_inventory() -> None:
    run_inventory_report()


def handle_network_demo() -> None:
    """Demostración de POO con modelos de red."""
    print("\n  ── Demo de modelos de red (POO) ──────────────")
    router = Router(hostname="core-router-01", ip="192.168.1.1", mac="AA:BB:CC:DD:EE:01", routing_protocol="OSPF")
    server = Server(hostname="web-server-01",  ip="192.168.1.10", mac="AA:BB:CC:DD:EE:10", os="Ubuntu 22.04", ram_gb=16)
    router.audit_device()
    server.audit_device()


def main() -> NoReturn:
    """Bucle principal del menú interactivo."""
    print_banner()
    while True:
        print_menu()
        opcion: str = input("  Elige una opción: ").strip()

        if   opcion == "1": handle_ping()
        elif opcion == "2": handle_disk()
        elif opcion == "3": handle_logs()
        elif opcion == "4": handle_threat()
        elif opcion == "5": handle_inventory()
        elif opcion == "6": handle_network_demo()
        elif opcion == "0":
            print("\n  👋 Hasta luego.\n")
            sys.exit(0)
        else:
            print("  ⚠ Opción no válida. Elige entre 0 y 6.")


if __name__ == "__main__":
    main()
