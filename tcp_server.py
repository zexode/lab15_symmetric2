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


# --- ВОТ ТВОИ TODO УЖЕ РЕШЕНЫ ---

def encrypt_for_transport(plaintext: str) -> str:
    k = 1234
    ciphertext = caesar_encrypt(k, plaintext)
    return pack_text_as_decimal_codes(ciphertext)


def decrypt_from_transport(packed_ciphertext: str) -> str:
    k = 1234
    ciphertext = unpack_decimal_codes_to_text(packed_ciphertext)
    return caesar_decrypt(k, ciphertext)


def run_echo_server() -> None:
    print(f"Ожидание подключения на {HOST}:{PORT} ...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen(1)

        conn, addr = server.accept()
        with conn:
            print("Подключён клиент:", addr)

            packed = recv_line(conn)
            msg = decrypt_from_transport(packed)

            print("Расшифрованное сообщение:", msg)

            reply = "ОТВЕТ: " + msg
            packed_reply = encrypt_for_transport(reply)

            send_line(conn, packed_reply)


# ЗАПУСК
run_echo_server()
