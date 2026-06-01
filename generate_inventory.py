"""
generate_inventory.py — Genera un inventario CSV de 1000 servidores ficticios.
Usa faker, csv y random para crear datos realistas de forma programática.
"""

import csv
import random
from faker import Faker

fake = Faker("es_ES")

# Configuración del inventario
OS_LIST: list[str] = [
    "Windows Server 2019",
    "Windows Server 2022",
    "Ubuntu 22.04 LTS",
    "Ubuntu 20.04 LTS",
    "CentOS 7",
    "Red Hat Enterprise 8",
    "Debian 11",
]

DEPARTMENTS: list[str] = [
    "IT",
    "Finanzas",
    "RRHH",
    "Operaciones",
    "Desarrollo",
    "Marketing",
    "Seguridad",
]

RAM_OPTIONS: list[int]  = [2, 4, 8, 16, 32, 64, 128]
CPU_OPTIONS: list[int]  = [2, 4, 8, 16, 32]
ROLES:       list[str]  = ["web", "db", "mail", "backup", "proxy", "monitoring", "storage"]


def generate_ip() -> str:
    """Genera una IP privada aleatoria."""
    return f"192.168.{random.randint(0, 254)}.{random.randint(1, 254)}"


def generate_inventory(output_path: str = "data/inventory.csv", rows: int = 1000) -> None:
    """
    Genera un archivo CSV con servidores ficticios.

    Args:
        output_path: Ruta del archivo CSV de salida.
        rows:        Número de filas a generar (por defecto 1000).
    """
    headers: list[str] = [
        "hostname", "ip", "os", "ram_gb", "cpu_cores",
        "department", "role", "last_update", "active"
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for i in range(1, rows + 1):
            dept  = random.choice(DEPARTMENTS)
            role  = random.choice(ROLES)
            writer.writerow({
                "hostname":    f"{dept.lower()[:3]}-{role}-{i:04d}",
                "ip":          generate_ip(),
                "os":          random.choice(OS_LIST),
                "ram_gb":      random.choice(RAM_OPTIONS),
                "cpu_cores":   random.choice(CPU_OPTIONS),
                "department":  dept,
                "role":        role,
                "last_update": fake.date_between(start_date="-3y", end_date="today").isoformat(),
                "active":      random.choice([True, True, True, False]),  # 75% activos
            })

    print(f"  ✅ Generado: {output_path} ({rows} filas)")


if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_inventory()
