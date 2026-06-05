# arp-mitm-lab
Lab ataque Man in the Middle mediante ARP

Eunice Y. Francisca Fleming 2024-1185

Enlace de video: (https://youtu.be/salMFzkmaRU)

Enlace de Playlist: https://www.youtube.com/playlist?list=PLedgCpC2B7oUOUOG7D6VLYsRR7i7bySIM

**Matrícula:** 2024-1185

---

## Descripción

Script Python que realiza un ataque **Man in the Middle (MitM)** mediante **ARP Poisoning**. El atacante envenena las tablas ARP de la víctima y el gateway simultáneamente, colocándose en medio de toda la comunicación sin que ninguno lo detecte.

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Linux (probado en Linux2024 / Debian) |
| Python | 3.x |
| Librería | Scapy (`pip3 install scapy`) |
| Privilegios | root (sudo) |
| IP Forwarding | `echo 1 > /proc/sys/net/ipv4/ip_forward` |
| Simulador | GNS3 con IOU Cisco |

---

## Instalación

```bash
pip3 install scapy
echo 1 > /proc/sys/net/ipv4/ip_forward
```

---

## Uso

```bash
sudo python3 arp_mitm.py -v <ip_victima> -g <ip_gateway> -i <interfaz> --verbose
```

### Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-v` / `--victim` | IP de la víctima | `-v 192.168.1.10` |
| `-g` / `--gateway` | IP del gateway | `-g 192.168.1.1` |
| `-i` / `--iface` | Interfaz de red | `-i eth0` |
| `-t` / `--interval` | Intervalo entre envíos (seg) | `-t 1.0` |
| `--verbose` | Mostrar cada paquete | `--verbose` |

### Ejemplo

```bash
sudo python3 arp_mitm.py -v 192.168.1.10 -g 192.168.1.1 -i eth0 --verbose
```

---

## Topología

```

```
<img width="620" height="594" alt="image" src="https://github.com/user-attachments/assets/d8a6f439-5a9e-47a6-bc05-f23dd0d0902f" />

### Tabla de Direccionamiento

| Dispositivo | IP | Máscara | Rol |
|-------------|-----|---------|-----|
| IOU1 | 192.168.1.1 | /24 | Gateway |
| WebTerm-1 | 192.168.1.10 | /24 | Víctima 1 |
| WebTerm-2 | 192.168.1.20 | /24 | Víctima 2 |
| Linux2024 | 192.168.1.30 | /24 | Atacante |

---

## Verificación

Antes del ataque

<img width="975" height="363" alt="image" src="https://github.com/user-attachments/assets/2588a013-ffdc-455a-93d7-bd6fe1dbb130" />

```bash
# En la víctima — debe mostrar MAC del atacante para el gateway
arp -a

# En el atacante — ver tráfico interceptado
tcpdump -i eth0 -n host 192.168.1.10
```
<img width="975" height="597" alt="image" src="https://github.com/user-attachments/assets/4223fd44-ba3d-4b86-8003-7f6776162eaa" />

<img width="830" height="214" alt="image" src="https://github.com/user-attachments/assets/fa65c2b2-bea4-4219-9765-5f1e91796b5a" />

---

## Contramedida

```bash
# ARP estático en el router
conf t
arp 192.168.1.10 0242.53bc.ef00 arpa
end

# ARP estático en la víctima
arp -s 192.168.1.1 aa:bb:cc:00:01:00
```


<img width="629" height="208" alt="image" src="https://github.com/user-attachments/assets/c7543542-5262-409b-abc7-9aec26d96105" />


<img width="663" height="110" alt="image" src="https://github.com/user-attachments/assets/149e40a5-bdea-4ce3-87d4-9e2efa9dbebd" />

---

## Video

> Enlace al video de demostración: [https://youtu.be/salMFzkmaRU]

---

## Documentación

Ver archivo `ARP_MitM_Documentacion.pdf` incluido en este repositorio.
