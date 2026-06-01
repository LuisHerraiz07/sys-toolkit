"""
scheduler.py — Demonio que ejecuta el análisis de inventario cada hora.
Usa la librería 'schedule' para programar tareas periódicas.
Ejecutar con: python scheduler.py
"""

import schedule
import time
import datetime
from inventory_manager import load_inventory, generate_excel_report


def tarea_inventario() -> None:
    """Tarea programada: carga el inventario y genera el informe Excel."""
    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n  ⏰ [{ahora}] Ejecutando análisis automático de inventario…")
    try:
        df = load_inventory()
        generate_excel_report(df)
        print(f"  ✅ Análisis completado correctamente.")
    except Exception as e:
        print(f"  ❌ Error en la tarea programada: {e}")


if __name__ == "__main__":
    print("\n  🕐 Demonio de inventario iniciado")
    print("  Ejecutará el análisis cada hora.")
    print("  Presiona Ctrl+C para detener.\n")

    # Programar la tarea cada hora
    schedule.every(1).hours.do(tarea_inventario)

    # Ejecutar una vez al arrancar
    tarea_inventario()

    # Bucle infinito del demonio
    while True:
        schedule.run_pending()
        time.sleep(60)
