import json

def send_message(s, data):
    payload = json.dumps(data).encode("utf-8")

    length = len(payload).to_bytes(4, "big")

    s.sendall(length)
    s.sendall(payload)

def receive_message(s):
    length_bytes = s.recv(4)

    if not length_bytes:
        return None

    length = int.from_bytes(length_bytes, "big")

    payload = b""
    while len(payload) < length:
        chunk = s.recv(length - len(payload))
        if not chunk:
            return None

        payload += chunk
    return json.loads(payload.decode("utf-8"))