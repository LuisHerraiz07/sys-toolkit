"""
os_utils.py — Utilidades de sistema operativo.
Ping a IPs y comprobación de espacio en disco.
"""

import os
import shutil
import subprocess
import platform
from typing import Optional


def check_ping(ip: str) -> bool:
    """
    Ejecuta un ping al sistema operativo para comprobar si una IP responde.
    Usa subprocess para llamar al comando nativo del SO.

    Args:
        ip: Dirección IP o hostname a comprobar.

    Returns:
        True si la IP responde, False si no.
    """
    # El parámetro varía según el sistema operativo
    param: str = "-n" if platform.system().lower() == "windows" else "-c"
    command: list[str] = ["ping", param, "1", ip]

    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except FileNotFoundError:
        # El comando ping no está disponible en este sistema
        return False


def check_disk_space(path: str = "/", threshold_pct: float = 20.0) -> Optional[dict[str, float]]:
    """
    Comprueba el espacio libre en disco de una partición.
    Lanza una alerta si el espacio libre es menor al umbral indicado.

    Args:
        path:          Ruta de la partición a comprobar.
        threshold_pct: Porcentaje mínimo de espacio libre (por defecto 20%).

    Returns:
        Diccionario con total, usado y libre en GB, o None si la ruta no existe.
    """
    if not os.path.exists(path):
        print(f"  ⚠ La ruta '{path}' no existe en este sistema.")
        return None

    usage = shutil.disk_usage(path)
    total_gb: float = usage.total / (1024 ** 3)
    used_gb:  float = usage.used  / (1024 ** 3)
    free_gb:  float = usage.free  / (1024 ** 3)
    free_pct: float = (usage.free / usage.total) * 100

    print(f"\n  📁 Partición: {path}")
    print(f"     Total:  {total_gb:.1f} GB")
    print(f"     Usado:  {used_gb:.1f} GB")
    print(f"     Libre:  {free_gb:.1f} GB ({free_pct:.1f}%)")

    if free_pct < threshold_pct:
        print(f"\n  🚨 ALERTA: Espacio libre ({free_pct:.1f}%) por debajo del umbral ({threshold_pct}%)")
        print(f"     Considera limpiar archivos en {path}")
    else:
        print(f"\n  ✅ Espacio en disco correcto ({free_pct:.1f}% libre)")

    return {"total_gb": total_gb, "used_gb": used_gb, "free_gb": free_gb, "free_pct": free_pct}
