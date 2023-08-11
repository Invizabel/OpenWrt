import binascii
import socket
import threading

def packet_thread(interface):
    sniffer_socket = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,socket.ntohs(3))
    sniffer_socket.bind((interface,0))
    while True:
        try:
            packet = sniffer_socket.recv(65536)
            data = binascii.hexlify(packet).decode()
            with open("/root/USB/hex_dump.txt", "a") as file:
                file.write(data + "\n")

        except OSError:
            continue

def packet_fox():
    interfaces = ["eth0","eth1","eth2"]
    for interface in interfaces:
        my_thread = threading.Thread(target=packet_thread, args=[interface]).start()

packet_fox()
