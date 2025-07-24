import socket
import os
from Cryptodome.Cipher import ChaCha20
from Cryptodome.Util.Padding import pad, unpad

# Конфигурация
SERVER_IP = "your_server_ip"
SERVER_PORT = 51820
KEY = b"32-byte-key-for-ChaCha20Poly1305"  # Замените на свой!


class VPNClient:
    def __init__(self):
        self.tun = self.create_tun_interface()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def create_tun_interface(self):
        """Создает TUN-интерфейс (кроссплатформенно)"""
        if os.name == "posix":  # macOS/Linux
            import pyroute2
            ipr = pyroute2.IPRoute()
            ipr.link("add", ifname="mytun", kind="tun")
            return ipr
        else:  # Windows
            import wintun
            return wintun.WinTun("mytun")

    def encrypt(self, data):
        """Шифрует данные ChaCha20"""
        cipher = ChaCha20.new(key=KEY)
        return cipher.nonce + cipher.encrypt(pad(data, 16))

    def decrypt(self, data):
        """Дешифрует данные"""
        nonce, ciphertext = data[:12], data[12:]
        cipher = ChaCha20.new(key=KEY, nonce=nonce)
        return unpad(cipher.decrypt(ciphertext), 16)

    def run(self):
        while True:
            # Чтение из TUN
            data = self.tun.read(1500)
            encrypted = self.encrypt(data)

            # Отправка на сервер
            self.sock.sendto(encrypted, (SERVER_IP, SERVER_PORT))

            # Получение ответа
            resp, _ = self.sock.recvfrom(1500)
            decrypted = self.decrypt(resp)

            # Запись в TUN
            self.tun.write(decrypted)


if __name__ == "__main__":
    vpn = VPNClient()
    vpn.run()