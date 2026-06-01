"""
threat_intel.py — Inteligencia de amenazas: geolocalización de IPs sospechosas.
Consulta la API pública ipinfo.io para obtener país y organización de cada IP.
"""

import requests
from typing import Optional


def geolocate_ip(ip: str) -> Optional[dict[str, str]]:
    """
    Consulta la API de ipinfo.io para obtener información geográfica de una IP.

    Args:
        ip: Dirección IP a consultar.

    Returns:
        Diccionario con country, org, city y region, o None si falla.
    """
    try:
        response = requests.get(
            f"https://ipinfo.io/{ip}/json",
            timeout=5,
            headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            data: dict = response.json()
            return {
                "ip":      data.get("ip",      ip),
                "country": data.get("country", "??"),
                "city":    data.get("city",    "Desconocida"),
                "org":     data.get("org",     "Desconocida"),
            }
        return None
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None
    except Exception:
        return None


def show_threat_table(ips: list[str], counts: dict[str, int]) -> None:
    """
    Muestra una tabla en consola con IP atacante, intentos, país y organización.

    Args:
        ips:    Lista de IPs a consultar.
        counts: Diccionario {ip: número_de_intentos}.
    """
    print(f"\n  🌍 TABLA DE AMENAZAS ({len(ips)} IPs consultadas)")
    print("  " + "─" * 72)
    print(f"  {'IP':<18} {'Intentos':>9}  {'País':>5}  {'Ciudad':<16}  {'Organización'}")
    print("  " + "─" * 72)

    for ip in ips:
        intentos: int = counts.get(ip, 0)
        print(f"  {ip:<18} {intentos:>9}  {'...':>5}  {'consultando...':<16}", end="\r")

        info = geolocate_ip(ip)
        if info:
            print(f"  {ip:<18} {intentos:>9}  {info['country']:>5}  {info['city']:<16}  {info['org']}")
        else:
            print(f"  {ip:<18} {intentos:>9}  {'??':>5}  {'Sin conexión':<16}  Sin datos")

    print("  " + "─" * 72)
