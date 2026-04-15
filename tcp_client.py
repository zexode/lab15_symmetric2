import socket

HOST = "127.0.0.1"
PORT = 9009


def pack_text_as_decimal_codes(s: str) -> str:
    return " ".join(str(ord(ch)) for ch in s)


def unpack_decimal_codes_to_text(s: str) -> str:
    s = s.strip()
    if s == "":
        return ""
    nums = [int(x) for x in s.split()]
    return "".join(chr(n % 65536) for n in nums)


def caesar_encrypt(k: int, m: str) -> str:
    return ''.join(chr((ord(ch) + k) % 65536) for ch in m)


def caesar_decrypt(k: int, c: str) -> str:
    return ''.join(chr((ord(ch) - k) % 65536) for ch in c)


def send_line(sock, line: str):
    sock.sendall((line + "\n").encode())


def recv_line(sock):
    buf = bytearray()
    while True:
        ch = sock.recv(1)
        if ch == b"\n":
            break
        buf.extend(ch)
    return buf.decode()


KEY = 1234


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    msg = input("Введите сообщение: ")

    enc = caesar_encrypt(KEY, msg)
    packed = pack_text_as_decimal_codes(enc)

    send_line(s, packed)

    data = recv_line(s)
    cipher = unpack_decimal_codes_to_text(data)
    response = caesar_decrypt(KEY, cipher)

    print("Ответ:", response)