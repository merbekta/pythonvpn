# setup_tun.py
import subprocess


def run_command(command):
    """Komutu çalıştır ve çıktı ile hata mesajlarını yazdır."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

def setup_tun():
    """TUN cihazını oluştur ve yapılandır."""
    commands = [
        "ip tuntap add dev tun0 mode tun",
        "ip link set up dev tun0",
        "ip addr add 10.0.0.1/24 dev tun0",
        "ip route add default via 10.0.0.1 dev tun0",
        "ip route add 85.237.211.148/32 via 192.168.1.1", 
        "resolvectl dns tun0 8.8.8.8",
        "ip link set dev tun0 mtu 1400",
        "ufw allow 9999/tcp" 
    ]
    for command in commands:
        run_command(command)

if __name__ == "__main__":
    setup_tun() 
 
