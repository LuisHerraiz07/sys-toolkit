"""
inventory_manager.py — Análisis de inventario con Pandas y generación de Excel.
Lee el CSV generado, filtra servidores vulnerables y exporta un informe ejecutivo.
"""

import os
import datetime
import pandas as pd
from generate_inventory import generate_inventory


def load_inventory(csv_path: str = "data/inventory.csv") -> pd.DataFrame:
    """
    Carga el inventario CSV en un DataFrame de Pandas.

    Args:
        csv_path: Ruta al archivo CSV.

    Returns:
        DataFrame con el inventario cargado.
    """
    if not os.path.exists(csv_path):
        print(f"  ⚠ No se encontró {csv_path}. Generando inventario...")
        os.makedirs("data", exist_ok=True)
        generate_inventory(csv_path)

    df = pd.read_csv(csv_path)
    print(f"  📂 Inventario cargado: {len(df)} servidores")
    return df


def filter_windows_servers(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra servidores con sistema operativo Windows Server."""
    return df[df["os"].str.contains("Windows Server", na=False)]


def filter_low_ram(df: pd.DataFrame, max_ram_gb: int = 4) -> pd.DataFrame:
    """Filtra servidores con RAM menor o igual al umbral indicado."""
    return df[df["ram_gb"] <= max_ram_gb]


def group_by_department(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa por departamento y cuenta cuántos servidores tiene cada área."""
    return df.groupby("department").size().reset_index(name="total_servers").sort_values("total_servers", ascending=False)


def generate_excel_report(df: pd.DataFrame, output_dir: str = "data") -> str:
    """
    Genera un informe Excel con múltiples hojas:
    - Resumen ejecutivo
    - Servidores Windows
    - Servidores con poca RAM
    - Distribución por departamento

    Args:
        df:         DataFrame con todos los servidores.
        output_dir: Directorio de salida del Excel.

    Returns:
        Ruta del archivo Excel generado.
    """
    os.makedirs(output_dir, exist_ok=True)
    fecha = datetime.date.today().strftime("%Y-%m")
    output_path = os.path.join(output_dir, f"informe-servidores-{fecha}.xlsx")

    windows_df    = filter_windows_servers(df)
    low_ram_df    = filter_low_ram(df)
    dept_df       = group_by_department(df)
    vulnerable_df = df[(df["os"].str.contains("Windows Server", na=False)) | (df["ram_gb"] <= 4)]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Hoja 1: Resumen ejecutivo
        resumen = pd.DataFrame({
            "Métrica":      ["Total servidores", "Servidores Windows", "Servidores con RAM ≤ 4GB", "Servidores vulnerables", "Servidores activos"],
            "Valor":        [len(df), len(windows_df), len(low_ram_df), len(vulnerable_df), df["active"].sum()],
        })
        resumen.to_excel(writer, sheet_name="Resumen", index=False)

        # Hoja 2: Windows Server
        windows_df.to_excel(writer, sheet_name="Windows Server", index=False)

        # Hoja 3: RAM baja
        low_ram_df.to_excel(writer, sheet_name="RAM Baja (≤4GB)", index=False)

        # Hoja 4: Por departamento
        dept_df.to_excel(writer, sheet_name="Por Departamento", index=False)

        # Hoja 5: Servidores vulnerables
        vulnerable_df.to_excel(writer, sheet_name="Vulnerables", index=False)

    print(f"  📊 Informe Excel generado: {output_path}")
    return output_path


def run_inventory_report() -> None:
    """Función principal que ejecuta el análisis completo."""
    print("\n  ── Análisis de inventario ────────────────────")
    df = load_inventory()

    windows = filter_windows_servers(df)
    low_ram = filter_low_ram(df)
    by_dept = group_by_department(df)

    print(f"\n  🪟 Servidores Windows Server: {len(windows)}")
    print(f"  📉 Servidores con RAM ≤ 4GB: {len(low_ram)}")
    print(f"\n  Distribución por departamento:")
    print("  " + "─" * 35)
    for _, row in by_dept.iterrows():
        print(f"  {row['department']:<15} {int(row['total_servers']):>4} servidores")

    excel_path = generate_excel_report(df)
    print(f"\n  ✅ Informe listo: {excel_path}")
