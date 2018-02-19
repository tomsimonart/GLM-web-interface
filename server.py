#!/usr/bin/env python3

import socket
import threading
from sys import argv
from time import sleep
from GLM.source.libs.rainbow import msg

SEP_CHAR = ';'
end = False

addr = "localhost"
port = 9999

if len(argv) >= 2 and argv[1].isdecimal():
    port = int(argv[1])

server_addr = (addr, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.setblocking(0)
server.bind(server_addr)
server.listen(5)

def handle(client, client_message=None, transmit=True):
    response = ""

    # Message is empty
    if client_message == None or client_message == ' ':
        response = "Empty message"

    # Message has the wrong format
    elif client_message.rfind(SEP_CHAR) < 0:
        response = "Bad message"

    else: # Decompose message
        msg(client_message)
        user = ""
        message = SEP_CHAR
        try:
            user, message = client_message.split(SEP_CHAR)
            if message == "close":
                transmit = False

            elif user == "web_client":
                msg("web client", 1)
                # client.send("hello web client".encode())
                response = "hello web client"
                # Processing web client requests
            elif user == "plugin":
                msg("plugin", 1)
                # client.send("hello plugin".encode())
                response = "hello plugin"
                # Processing plugin requests
            else:
                msg("bad user", 2)
                # client.send("bad user".encode())
                response = "bad user"
        except IndexError:
            # client.send("wrong format".encode())
            response = "bad user"

    return response, transmit

def handle_client():
    global end

    # Accepting client connection
    client, addr = server.accept()
    msg("New client", 0, "Server", addr, client)

    transmit = True
    while transmit:
        # Getting client packet
        received = False
        while not received:
            client_message = client.recv(512).decode()
            if len(client_message) > 0:
                received = True
        msg("Message", 0, "Client", client_message)

        if client_message == "exit": # Close server
            client.send("[*] Terminating".encode()) # Last message
            client.close()
            sleep(1)
            transmit = False
            end = True

        else:
            # Answering to client after handle
            response, transmit = handle(client, client_message, transmit)
            client.send(response.encode())
            msg("Response", 0, "Server", response)

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
                server.close()
                msg("Terminating",  2, "Server")
                break
    except KeyboardInterrupt:
        print()
        msg("Interruption", 3, "Server", server)
        server.close()
