"""
test_toolkit.py — Tests unitarios para sys-toolkit.
Ejecutar con: pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from log_parser    import parse_auth_log, count_failed_ips, get_top_attackers
from network_models import Router, Server, NetworkDevice
from os_utils       import check_disk_space


# ── Fixtures ────────────────────────────────────────────────────

@pytest.fixture
def sample_log_file(tmp_path):
    """Crea un auth.log de prueba en un directorio temporal."""
    log = tmp_path / "auth.log"
    log.write_text(
        "Jan 01 10:00:01 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2\n"
        "Jan 01 10:00:02 server sshd[1235]: Failed password for admin from 10.0.0.1 port 22 ssh2\n"
        "Jan 01 10:00:03 server sshd[1236]: Failed password for root from 192.168.1.100 port 22 ssh2\n"
        "Jan 01 10:00:04 server sshd[1237]: Invalid user oracle from 172.16.0.1 port 22\n"
        "Jan 01 10:00:05 server sshd[1238]: Accepted password for deploy from 192.168.1.50 port 22 ssh2\n"
        "Jan 01 10:00:06 server sshd[1239]: Failed password for test from 192.168.1.100 port 22 ssh2\n"
    )
    return str(log)


# ── Tests: log_parser ────────────────────────────────────────────

class TestLogParser:

    def test_parse_returns_failed_ips(self, sample_log_file):
        """Debe detectar las IPs con intentos fallidos."""
        failed, _ = parse_auth_log(sample_log_file)
        assert len(failed) == 4
        assert "192.168.1.100" in failed
        assert "10.0.0.1" in failed

    def test_parse_detects_invalid_users(self, sample_log_file):
        """Debe detectar IPs de usuarios inválidos."""
        failed, _ = parse_auth_log(sample_log_file)
        assert "172.16.0.1" in failed

    def test_parse_returns_successful_ips(self, sample_log_file):
        """Debe detectar los accesos exitosos."""
        _, success = parse_auth_log(sample_log_file)
        assert len(success) == 1
        assert "192.168.1.50" in success

    def test_count_failed_ips(self, sample_log_file):
        """Debe contar correctamente los intentos por IP."""
        failed, _ = parse_auth_log(sample_log_file)
        counts = count_failed_ips(failed)
        assert counts["192.168.1.100"] == 3
        assert counts["10.0.0.1"] == 1
        assert counts["172.16.0.1"] == 1

    def test_count_uses_unique_ips(self):
        """El Set debe eliminar duplicados antes de contar."""
        ips = ["1.1.1.1", "1.1.1.1", "2.2.2.2", "1.1.1.1"]
        counts = count_failed_ips(ips)
        assert counts["1.1.1.1"] == 3
        assert counts["2.2.2.2"] == 1
        assert len(counts) == 2

    def test_get_top_attackers_order(self):
        """Debe devolver las IPs ordenadas de mayor a menor intentos."""
        counts = {"1.1.1.1": 5, "2.2.2.2": 10, "3.3.3.3": 1}
        top = get_top_attackers(counts, top_n=2)
        assert top[0] == ("2.2.2.2", 10)
        assert top[1] == ("1.1.1.1", 5)

    def test_file_not_found(self):
        """Debe lanzar FileNotFoundError si el archivo no existe."""
        with pytest.raises(FileNotFoundError):
            parse_auth_log("/ruta/inexistente/auth.log")

    def test_empty_log(self, tmp_path):
        """Un log vacío debe devolver listas vacías."""
        log = tmp_path / "empty.log"
        log.write_text("")
        failed, success = parse_auth_log(str(log))
        assert failed  == []
        assert success == []


# ── Tests: network_models ────────────────────────────────────────

class TestNetworkModels:

    def test_router_creation(self):
        """Debe crear un Router con los atributos correctos."""
        r = Router("router-01", "192.168.1.1", "AA:BB:CC:DD:EE:01", "OSPF")
        assert r.hostname == "router-01"
        assert r.ip       == "192.168.1.1"
        assert r.routing_protocol == "OSPF"

    def test_server_creation(self):
        """Debe crear un Server con los atributos correctos."""
        s = Server("web-01", "10.0.0.1", "AA:BB:CC:DD:EE:02", "Ubuntu 22.04", 16)
        assert s.ram_gb == 16
        assert s.os     == "Ubuntu 22.04"

    def test_base_class_audit_raises(self):
        """La clase base debe lanzar NotImplementedError."""
        device = NetworkDevice("dev", "1.1.1.1", "AA:AA:AA:AA:AA:AA")
        with pytest.raises(NotImplementedError):
            device.audit_device()

    def test_router_is_network_device(self):
        """Router debe ser instancia de NetworkDevice (herencia)."""
        r = Router("r", "1.1.1.1", "AA:AA:AA:AA:AA:AA", "BGP")
        assert isinstance(r, NetworkDevice)

    def test_server_is_network_device(self):
        """Server debe ser instancia de NetworkDevice (herencia)."""
        s = Server("s", "1.1.1.1", "AA:AA:AA:AA:AA:AA", "Debian", 8)
        assert isinstance(s, NetworkDevice)


# ── Tests: os_utils ──────────────────────────────────────────────

class TestOsUtils:

    def test_disk_space_returns_dict(self, tmp_path):
        """check_disk_space debe devolver un diccionario con las métricas."""
        result = check_disk_space(str(tmp_path))
        assert result is not None
        assert "total_gb" in result
        assert "free_pct" in result
        assert result["total_gb"] > 0

    def test_disk_space_invalid_path(self):
        """Una ruta inexistente debe devolver None."""
        result = check_disk_space("/ruta/que/no/existe/jamás")
        assert result is None
