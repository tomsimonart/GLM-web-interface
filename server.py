#!/usr/bin/env python3

import socket
import threading
from sys import argv
from time import sleep
from GLM.source.libs.rainbow import msg

end = False

addr = "localhost"
port = 9999

if len(argv) >= 2 and argv[1].isdecimal():
    port = int(argv[1])

server_addr = (addr, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_addr)
server.listen(5)

def handle_client():
    global end

    # Accepting client connection
    client, addr = server.accept()
    msg("New client", 0, "Server", addr)

    # Getting client packet
    client_message = client.recv(512).decode()
    msg("Message", 0, "Client", client_message)

    if client_message == "exit":
        msg("Terminating",  2, "Server")
        client.send("[*] Terminating".encode()) # Last message
        server.close()
        end = True
        return None

    else:
        client.send("[*] Received: {}".format(client_message).encode())


    return None

if __name__ == "__main__":
    try:
        msg("Starting", 0, "Server", server_addr)
        while True:
            if not end:
                client_handler = threading.Thread(target=handle_client, args=(), daemon=True)
                client_handler.start()
                client_handler.join() # Waiting for thread to end
            else:
                break
    except KeyboardInterrupt:
        print()
        msg("Interruption", 3, "Server", server)
        server.close()
