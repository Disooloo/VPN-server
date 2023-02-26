import os
import socket
import fcntl
import struct

# установка IP-адреса и маски сети для TUN-интерфейса
TUN_IP = '10.0.0.1'
TUN_MASK = '255.255.255.0'

# создание TUN-интерфейса
tun = os.open('/dev/net/tun', os.O_RDWR)
ifr = struct.pack('16sH', b'tun%d', 0x0001)
ifr = fcntl.ioctl(tun, 0x400454ca, ifr)
ifname = ifr[:16].strip(b'\x00').decode('utf8')

# настройка IP-адреса и маски сети для TUN-интерфейса
os.system(f'ifconfig {ifname} {TUN_IP} netmask {TUN_MASK} up')

# создание сокета для VPN-сервера
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 1194))

# принятие входящих пакетов и отправка их в TUN-интерфейс
while True:
    data, client_addr = sock.recvfrom(2048)
    os.write(tun, data)