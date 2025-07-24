import socket
from Cryptodome.Cipher import ChaCha20

KEY = b"32-byte-key-for-ChaCha20Poly1305"  # Должен совпадать с клиентом!


class VPNServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 51820))

    def decrypt(self, data):
        nonce, ciphertext = data[:12], data[12:]
        cipher = ChaCha20.new(key=KEY, nonce=nonce)
        return cipher.decrypt(ciphertext)

    def encrypt(self, data):
        cipher = ChaCha20.new(key=KEY)
        return cipher.nonce + cipher.encrypt(data)

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1500)
            decrypted = self.decrypt(data)

            # Здесь можно отправить трафик в интернет
            # Например, через requests или raw sockets

            # Эхо-ответ для теста
            encrypted_resp = self.encrypt(decrypted)
            self.sock.sendto(encrypted_resp, addr)


if __name__ == "__main__":
    server = VPNServer()
    server.run()