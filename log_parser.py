"""
log_parser.py — Analizador de logs de autenticación SSH.
Lee auth.log línea a línea usando gestores de contexto para no saturar la RAM.
"""

import re
from typing import Tuple


# Patrones de expresiones regulares para detectar eventos SSH
_PATTERN_FAILED:  re.Pattern[str] = re.compile(
    r"Failed password for .+ from (\d+\.\d+\.\d+\.\d+)"
)
_PATTERN_INVALID: re.Pattern[str] = re.compile(
    r"Invalid user .+ from (\d+\.\d+\.\d+\.\d+)"
)
_PATTERN_SUCCESS: re.Pattern[str] = re.compile(
    r"Accepted password for .+ from (\d+\.\d+\.\d+\.\d+)"
)


def parse_auth_log(filepath: str) -> Tuple[list[str], list[str]]:
    """
    Analiza un archivo auth.log de Linux y extrae las IPs.
    Usa 'with open' para leer línea a línea sin cargar el archivo completo en RAM.

    Args:
        filepath: Ruta al archivo auth.log.

    Returns:
        Tupla de (lista de IPs fallidas, lista de IPs exitosas).

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    failed_ips:     list[str] = []
    successful_ips: list[str] = []

    # El gestor de contexto garantiza que el archivo se cierra aunque haya un error
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            # Intentos fallidos
            match_failed  = _PATTERN_FAILED.search(line)
            match_invalid = _PATTERN_INVALID.search(line)
            if match_failed:
                failed_ips.append(match_failed.group(1))
            elif match_invalid:
                failed_ips.append(match_invalid.group(1))

            # Accesos exitosos
            match_success = _PATTERN_SUCCESS.search(line)
            if match_success:
                successful_ips.append(match_success.group(1))

    return failed_ips, successful_ips


def count_failed_ips(failed_ips: list[str]) -> dict[str, int]:
    """
    Cuenta cuántas veces ha fallado cada IP usando un Set para deduplicar
    y un diccionario para el conteo.

    Args:
        failed_ips: Lista de IPs (puede contener duplicados).

    Returns:
        Diccionario {ip: número_de_intentos}.
    """
    # El Set elimina duplicados automáticamente — útil para saber cuántas IPs únicas hay
    unique_ips: set[str] = set(failed_ips)

    # El diccionario cuenta los intentos de cada IP única
    counts: dict[str, int] = {}
    for ip in unique_ips:
        counts[ip] = failed_ips.count(ip)

    return counts


def get_top_attackers(counts: dict[str, int], top_n: int = 10) -> list[tuple[str, int]]:
    """
    Devuelve las N IPs con más intentos fallidos.

    Args:
        counts: Diccionario {ip: intentos}.
        top_n:  Número de IPs a devolver.

    Returns:
        Lista de tuplas (ip, intentos) ordenada de mayor a menor.
    """
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
