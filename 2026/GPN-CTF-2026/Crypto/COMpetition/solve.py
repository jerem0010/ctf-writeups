from hashlib import sha256
import socket
import ssl

HOST = "pickled-chorizo-atop-smashed-truffle-oil-nxsl.gpn24.ctf.kitctf.de"
PORT = 443

context = ssl.create_default_context()

with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname=HOST) as s:
        for i in range(100):
            data = b""
            while b"Commitment (hex): " not in data:
                data += s.recv(4096)
            print(data.decode(errors="ignore"), end="")

            blob = f"round-{i}-AAArockBBBpaperCCCscissorsDDD".encode()
            com = sha256(blob).hexdigest()
            s.sendall(com.encode() + b"\n")

            data = b""
            while b"What did you choose? " not in data:
                data += s.recv(4096)

            text = data.decode(errors="ignore")
            print(text, end="")

            if "I choose rock." in text:
                my_choice = "paper"
            elif "I choose paper." in text:
                my_choice = "scissors"
            elif "I choose scissors." in text:
                my_choice = "rock"
            else:
                raise Exception("Choix serveur non trouvé")

            s.sendall(my_choice.encode() + b"\n")

            msg = my_choice.encode()
            pos = blob.index(msg)

            r1 = blob[:pos]
            r2 = blob[pos + len(msg):]

            data = b""
            while b"Proof (hex): " not in data:
                data += s.recv(4096)
            print(data.decode(errors="ignore"), end="")

            proof = r1.hex() + " " + r2.hex()
            s.sendall(proof.encode() + b"\n")

        final = s.recv(4096)
        print(final.decode(errors="ignore"))