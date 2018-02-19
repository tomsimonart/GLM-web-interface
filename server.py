#!/usr/bin/env python3

import socket
import threading
from sys import argv
from time import sleep
from GLM.source.libs.rainbow import msg

SEP_CHAR = ';'
BUFFSIZE = 512
end = False

addr = "localhost"
port = 9999

if len(argv) >= 2 and argv[1].isdecimal():
    port = int(argv[1])

server_addr = (addr, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Re-use port
server.bind(server_addr)
server.listen(5)

# def handle(client, client_message, user, transmit):
#     msg("handle", 3)
#     response = "" # Will be sent back to client
#
#     # Message is empty
#     if client_message == None or client_message == ' ':
#         response = "Empty message"
#
#     # Message has the wrong format
#     elif client_message.rfind(SEP_CHAR) < 0:
#         response = "Bad message"
#
#     else: # Decompose message
#         msg(client_message)
#         user = ""
#         message = SEP_CHAR
#         try:
#             user, message = client_message.split(SEP_CHAR)
#             if message == "close":
#                 transmit = False
#
#             elif user == "web_client":
#                 msg("web client", 1)
#                 response = "<a>tperale</a>"
#                 # Processing web client requests
#             elif user == "plugin":
#                 msg("plugin", 1)
#                 response = "hello plugin"
#                 # Processing plugin requests
#             else:
#                 msg("bad user", 2)
#                 response = "bad user"
#         except IndexError:
#             response = "bad user"
#
#     return response, transmit

def handle(client, user, transmit):
    response = " " # Will be sent to client
    client_request = client.recv(BUFFSIZE).decode() # 2 recv

    # Plugin
    if user == "plugin":
        response = "plugin handle"

    # Web client
    elif user == "web_client":
        response = "web_client handle"

    else:
        transmit = False

    transmit = False

    return response, transmit

def handle_client(client, addr, user):
    global end

    transmit = True
    while transmit:
        response, transmit = handle(client, user, transmit)
        msg("Responding", 3, response, addr)
        client.send(response.encode())

    return None

if __name__ == "__main__":
    try:
        msg("Starting", 1, "Server", server_addr)
        while True:
            if not end:
                # Accepting client connection
                client, addr = server.accept()
                user = client.recv(BUFFSIZE).decode() # 1 recv
                msg("New client", 1, "Server", addr)

                # Check if user is a possible name
                if user == "plugin" or user == "web_client":
                    # User accepted
                    client.send(b"a:client_connected")
                    msg("Accepted", 1, "Server", user)
                else:
                    # Bad user
                    client.send(b"e:bad_user")
                    msg("Refused", 2, "Server", user)

                client_handler = threading.Thread(
                    name=user,
                    target=handle_client,
                    args=(client, addr, user),
                    daemon=True
                    )
                client_handler.start()
            else:
                server.close()
                msg("Terminating",  2, "Server")
                break
    except KeyboardInterrupt:
        print()
        # traceback.print_exc()
        msg("Interruption", 3, "Server", server)
        server.close()
