#!/usr/bin/env python3
"""
TCP-сервер (эхо «ОТВЕТ: …») + общий код: Цезарь mod 65536 и строка кодов для сокета.
Клиент (client.py) импортирует функции отсюда — один источник правды для ключа и формата.
"""
import socket

# --- общие константы (как в lab_symmetric_ciphers_ru.ipynb) ---
UNICODE_MOD = 65536
CAESAR_K = 1234
HOST = "127.0.0.1"
PORT = 9009


def _wrap(x: int) -> int:
    return x % UNICODE_MOD


def caesar_encrypt(k: int, m: str) -> str:
    return "".join(chr(_wrap(ord(c) + k)) for c in m)


def caesar_decrypt(k: int, c: str) -> str:
    return "".join(chr(_wrap(ord(c) - k)) for c in c)


def pack_text_as_decimal_codes(s: str) -> str:
    return " ".join(str(ord(c)) for c in s)


def unpack_decimal_codes_to_text(s: str) -> str:
    s = s.strip()
    if not s:
        return ""
    return "".join(chr(_wrap(int(x))) for x in s.split())


def encrypt_for_transport(plain: str, k: int = CAESAR_K) -> str:
    return pack_text_as_decimal_codes(caesar_encrypt(k, plain))


def decrypt_from_transport(packed: str, k: int = CAESAR_K) -> str:
    return caesar_decrypt(k, unpack_decimal_codes_to_text(packed))


def send_line(sock: socket.socket, line: str) -> None:
    sock.sendall((line + "\n").encode("utf-8"))


def recv_line(sock: socket.socket) -> str:
    buf = bytearray()
    while True:
        b = sock.recv(1)
        if not b:
            raise ConnectionError("соединение закрыто")
        if b == b"\n":
            break
        buf.extend(b)
    return buf.decode("utf-8")


# --- настройки сервера ---
HOST_BIND = HOST
PORT_BIND = PORT
KEY = CAESAR_K


def main() -> None:
    print(f"Сервер: {HOST_BIND}:{PORT_BIND}, ключ k={KEY}")
    print("Ожидание одного подключения…")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST_BIND, PORT_BIND))
    server.listen(1)

    conn, addr = server.accept()
    server.close()

    print("Клиент:", addr)

    packed = recv_line(conn)
    print("Строка из сокета (начало):", packed[:80] + ("…" if len(packed) > 80 else ""))

    msg = decrypt_from_transport(packed, KEY)
    print("Расшифровано:", msg)

    reply = "ОТВЕТ: " + msg
    send_line(conn, encrypt_for_transport(reply, KEY))
    conn.close()
    print("Ответ отправлен, сервер завершён.")


if __name__ == "__main__":
    main()
