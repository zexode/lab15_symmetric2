#!/usr/bin/env python3
"""Клиент: отправка сообщения и приём ответа. Общая криптология — в server.py (импорт)."""
import socket
import sys

from server import (
    CAESAR_K,
    HOST,
    PORT,
    caesar_encrypt,
    decrypt_from_transport,
    encrypt_for_transport,
    pack_text_as_decimal_codes,
    recv_line,
    send_line,
)

SERVER_HOST = HOST
SERVER_PORT = PORT
KEY = CAESAR_K


def main() -> None:
    if len(sys.argv) > 1:
        message = " ".join(sys.argv[1:])
    else:
        print("Введите сообщение (Enter — пример по умолчанию).")
        message = input("> ").strip() or "Привет, сервер"

    print()
    print("1) Открытый текст:", message)
    cipher = caesar_encrypt(KEY, message)
    print("2) После Цезаря (k=%d), первые символы: %r" % (KEY, cipher[:40]))
    on_wire = pack_text_as_decimal_codes(cipher)
    print("3) В TCP уходит строка кодов (начало):", on_wire[:80] + ("…" if len(on_wire) > 80 else ""))
    print()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_HOST, SERVER_PORT))

    send_line(sock, encrypt_for_transport(message, KEY))
    packed_reply = recv_line(sock)
    sock.close()

    reply = decrypt_from_transport(packed_reply, KEY)
    print("Ответ сервера (расшифровано):", reply)


if __name__ == "__main__":
    main()
