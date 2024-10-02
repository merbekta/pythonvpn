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
        "ip addr add 10.0.0.2/24 dev tun0",
        "ip link set dev tun0 mtu 1400",
        "iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE",
        "iptables -A INPUT -i tun0 -j ACCEPT",
        "iptables -A FORWARD -i tun0 -o enp0s3 -j ACCEPT",
        "iptables -A FORWARD -i enp0s3 -o tun0 -j ACCEPT",
        "sysctl -w net.ipv4.ip_forward=1",
        "ufw allow 9999/tcp" 
    ]
    for command in commands:
        run_command(command)

if __name__ == "__main__":
    setup_tun() 
