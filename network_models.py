"""
network_models.py — Modelos orientados a objetos para dispositivos de red.
Demuestra herencia, polimorfismo y encapsulación con dispositivos de red reales.
"""


class NetworkDevice:
    """
    Clase base para cualquier dispositivo de red.
    Define la interfaz común que deben implementar todos los dispositivos.
    """

    def __init__(self, hostname: str, ip: str, mac: str) -> None:
        self.hostname: str = hostname
        self.ip:       str = ip
        self.mac:      str = mac

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(hostname={self.hostname!r}, ip={self.ip!r})"

    def audit_device(self) -> None:
        """
        Método polimórfico: cada subclase implementa su propia auditoría.
        La clase base lanza NotImplementedError para forzar la implementación.
        """
        raise NotImplementedError("Cada dispositivo debe implementar su propia auditoría.")

    def print_info(self) -> None:
        """Muestra información básica del dispositivo."""
        print(f"\n  {'─' * 45}")
        print(f"  Dispositivo: {self.__class__.__name__}")
        print(f"  Hostname:    {self.hostname}")
        print(f"  IP:          {self.ip}")
        print(f"  MAC:         {self.mac}")


class Router(NetworkDevice):
    """
    Dispositivo de red: Router.
    Hereda de NetworkDevice y añade atributos específicos de routing.
    """

    def __init__(self, hostname: str, ip: str, mac: str, routing_protocol: str) -> None:
        super().__init__(hostname, ip, mac)
        self.routing_protocol: str = routing_protocol

    def audit_device(self) -> None:
        """
        Auditoría específica para routers.
        Polimorfismo: el mismo método, comportamiento distinto según la clase.
        """
        self.print_info()
        print(f"  Protocolo:   {self.routing_protocol}")
        print(f"\n  🔒 DIRECTRICES DE SEGURIDAD (Router)")
        print(f"     ✓ Deshabilitar telnet — usar solo SSH v2")
        print(f"     ✓ Activar listas de control de acceso (ACL)")
        print(f"     ✓ Actualizar firmware del fabricante")
        print(f"     ✓ Revisar tablas de routing {self.routing_protocol} periódicamente")
        print(f"     ✓ Habilitar logging hacia servidor syslog central")


class Server(NetworkDevice):
    """
    Dispositivo de red: Servidor.
    Hereda de NetworkDevice y añade atributos específicos de servidor.
    """

    def __init__(self, hostname: str, ip: str, mac: str, os: str, ram_gb: int) -> None:
        super().__init__(hostname, ip, mac)
        self.os:     str = os
        self.ram_gb: int = ram_gb

    def audit_device(self) -> None:
        """Auditoría específica para servidores."""
        self.print_info()
        print(f"  Sistema OS:  {self.os}")
        print(f"  RAM:         {self.ram_gb} GB")
        print(f"\n  🔒 DIRECTRICES DE SEGURIDAD (Servidor)")
        print(f"     ✓ Aplicar parches de seguridad pendientes en {self.os}")
        print(f"     ✓ Revisar usuarios con acceso root/sudo")
        print(f"     ✓ Comprobar puertos abiertos con netstat o ss")
        print(f"     ✓ Revisar logs en /var/log/auth.log")
        print(f"     ✓ Verificar configuración del firewall (ufw/iptables)")
        if self.ram_gb < 8:
            print(f"     ⚠ RAM baja ({self.ram_gb}GB) — considerar ampliar para producción")
