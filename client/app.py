#################################################
import socket
import os
import fcntl
import struct
import threading

SERVER_IP = "85.237.211.148"
SERVER_PORT = 9999
TUN_INTERFACE = '/dev/net/tun'
TUNSETIFF = 0x400454ca
IFF_TUN = 0x0001
IFF_NO_PI = 0x1000

# TUN arayüzünü yapılandır 
def create_tun():
    tun = os.open(TUN_INTERFACE, os.O_RDWR)
    ifr = struct.pack('16sH', b'tun0', IFF_TUN | IFF_NO_PI)
    fcntl.ioctl(tun, TUNSETIFF, ifr)
    print("TUN CREATED") 
    return tun

# Bağlantı kurma
def socket_to_tun(tun,client_socket): 
    while True:
        try:
            # Veriyi al
            data = client_socket.recv(1400) 
            if data: 
                # Veriyi TUN arayüzüne yaz
                os.write(tun,data)
                print(data)
                print("Write to TUN") 
        except Exception as e:
            print(f"tun_to_client Error: {e}") 

# Bağlantı kurma
def tun_to_socket(tun,client_socket): 
    print("client_to_tun READY")
    while True:
        print("FFFF")
        try: 
            data = os.read(tun,1400) 
            if data:
                # Veriyi sunucuya gönder 
                client_socket.send(data)
                print("Send to client:") 
        except Exception as e:
            print(f"client_to_tun Error: {e}") 


def main():
    print("START") 
    tun = create_tun()
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

     
    tun_to_client_thread = threading.Thread(target=tun_to_socket, args=(tun,client_socket,))
    client_to_tun_thread = threading.Thread(target=socket_to_tun, args=(tun,client_socket,))
    tun_to_client_thread.start()
    client_to_tun_thread.start() 
 
if __name__ == "__main__":
    main() 
