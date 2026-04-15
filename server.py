import socket

HOST = "127.0.0.1"
PORT = 65432
KEY = 1234


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
        if ch == b"":
            break
        if ch == b"\n":
            break
        buf.extend(ch)
    return buf.decode()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Server started on port", PORT)

    conn, addr = s.accept()
    with conn:
        print("Connected:", addr)

        while True:
            data = recv_line(conn)
            if not data:
                break

            cipher = unpack_decimal_codes_to_text(data)
            plaintext = caesar_decrypt(KEY, cipher)

            print("Получено:", plaintext)

            response = "echo: " + plaintext
            enc = caesar_encrypt(KEY, response)
            packed = pack_text_as_decimal_codes(enc)

            send_line(conn, packed)