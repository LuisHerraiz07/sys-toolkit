"""
generate_sample_log.py — Genera un auth.log de muestra con intentos SSH.
Ejecutar con: python data/generate_sample_log.py
"""

import random
import os

ATTACKER_IPS: list[str] = [
    "185.220.101.45", "45.33.32.156", "192.241.231.218",
    "198.199.122.249", "159.89.49.95",  "138.197.206.27",
    "104.131.191.87",  "64.227.27.48",  "167.172.173.96",
    "157.230.242.133",
]

LEGIT_IPS: list[str] = [
    "192.168.1.10", "192.168.1.20", "10.0.0.5",
]

USERS_INVALID: list[str] = ["admin", "root", "ubuntu", "oracle", "mysql", "test"]
USERS_VALID:   list[str] = ["sysadmin", "devops", "deploy"]

MONTHS  = ["Jan", "Feb", "Mar", "Apr", "May"]
DAYS    = [f"{i:02d}" for i in range(1, 29)]
HOSTS   = ["server01", "web-prod", "db-server"]

LOG_LINES: list[str] = []

for _ in range(2000):
    month  = random.choice(MONTHS)
    day    = random.choice(DAYS)
    hour   = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
    host   = random.choice(HOSTS)
    ip     = random.choice(ATTACKER_IPS)
    user   = random.choice(USERS_INVALID)
    port   = random.randint(1024, 65535)
    LOG_LINES.append(f"{month} {day} {hour} {host} sshd[{port}]: Failed password for {user} from {ip} port {port} ssh2")

for _ in range(500):
    month = random.choice(MONTHS)
    day   = random.choice(DAYS)
    hour  = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
    host  = random.choice(HOSTS)
    ip    = random.choice(ATTACKER_IPS)
    user  = random.choice(USERS_INVALID)
    port  = random.randint(1024, 65535)
    LOG_LINES.append(f"{month} {day} {hour} {host} sshd[{port}]: Invalid user {user} from {ip} port {port}")

for _ in range(50):
    month = random.choice(MONTHS)
    day   = random.choice(DAYS)
    hour  = f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
    host  = random.choice(HOSTS)
    ip    = random.choice(LEGIT_IPS)
    user  = random.choice(USERS_VALID)
    port  = random.randint(1024, 65535)
    LOG_LINES.append(f"{month} {day} {hour} {host} sshd[{port}]: Accepted password for {user} from {ip} port {port} ssh2")

random.shuffle(LOG_LINES)

os.makedirs(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", exist_ok=True)
output = os.path.join(os.path.dirname(__file__) if os.path.dirname(__file__) else ".", "auth.log")

with open(output, "w") as f:
    f.write("\n".join(LOG_LINES) + "\n")

print(f"✅ Generado: {output} ({len(LOG_LINES)} líneas)")
