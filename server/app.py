#################################################
import socket
import os
import fcntl
import struct
import threading

SERVER_IP = '0.0.0.0'
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
def tun_to_client(tun,client_socket): 
    while True:
        try:
            # Veriyi al
            data = client_socket.recv(1400) 
            # Veriyi TUN arayüzüne yaz
            if data: 
                os.write(tun,data)
                print(data)
                print("Write to TUN")
        except Exception as e:
            print(f"76 Error: {e}") 

# Bağlantı kurma
def client_to_tun(tun,client_socket): 
    print("client_to_tun READY")
    while True: 
        try: 
            data = os.read(tun,1400) 
            if data:
                # Veriyi sunucuya gönder
                client_socket.send(data)
                print("Send to client:") 
        except Exception as e:
            print(f"90 Error: {e}") 


def main():
    print("START") 

    tun = create_tun()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
         
        tun_to_client_thread = threading.Thread(target=tun_to_client, args=(tun,client_socket,))
        client_to_tun_thread = threading.Thread(target=client_to_tun, args=(tun,client_socket,))
        tun_to_client_thread.start()
        client_to_tun_thread.start() 

if __name__ == "__main__":
    main() 
