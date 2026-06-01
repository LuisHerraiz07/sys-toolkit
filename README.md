![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

# 🛡 SYS-TOOLKIT — Kit para Administradores de Sistemas

Herramientas en Python para administradores de red: auditoría de logs SSH, análisis de inventario, geolocalización de IPs y generación de informes Excel.

---

## Módulos

| Módulo | Descripción |
|---|---|
| `sys_toolkit.py` | Menú principal CLI interactivo |
| `os_utils.py` | Ping y comprobación de espacio en disco |
| `log_parser.py` | Análisis de auth.log SSH |
| `network_models.py` | Modelos de red con POO (Router, Server) |
| `threat_intel.py` | Geolocalización de IPs con ipinfo.io |
| `generate_inventory.py` | Genera 1000 servidores ficticios en CSV |
| `inventory_manager.py` | Análisis con Pandas + exportar a Excel |
| `scheduler.py` | Demonio que ejecuta análisis cada hora |

---

## Instalación

```bash
# Clonar repositorio
git clone https://github.com/LuisHerraiz07/sys-toolkit.git
cd sys-toolkit

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## Uso

```bash
# Menú principal interactivo
python sys_toolkit.py

# Generar log de prueba
python data/generate_sample_log.py

# Generar inventario CSV
python generate_inventory.py

# Ejecutar tests
pytest tests/ -v

# Demonio automático (cada hora)
python scheduler.py
```

---

## Tests

```bash
pytest tests/ -v
```

Salida esperada:
```
tests/test_toolkit.py::TestLogParser::test_parse_returns_failed_ips PASSED
tests/test_toolkit.py::TestLogParser::test_count_failed_ips PASSED
tests/test_toolkit.py::TestNetworkModels::test_router_creation PASSED
...
```

---

## Estructura

```
sys-toolkit/
├── sys_toolkit.py          # Menú CLI principal
├── os_utils.py             # Ping + disco
├── log_parser.py           # Parseo de auth.log
├── network_models.py       # POO: Router, Server
├── threat_intel.py         # API ipinfo.io
├── generate_inventory.py   # Generador de CSV
├── inventory_manager.py    # Pandas + Excel
├── scheduler.py            # Demonio automático
├── requirements.txt
├── .gitignore
├── data/
│   └── generate_sample_log.py
├── tests/
│   └── test_toolkit.py
└── docs/
    └── python-sysadmin.md
```

---

*Desarrollado durante las prácticas en [Corner Estudios](https://www.corner-estudios.com) — Luis Herraiz — 2026*
