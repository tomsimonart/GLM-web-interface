#!/usr/bin/env python3

import json
import socket
import threading
from sys import argv
from time import sleep
from queue import Queue
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


def handle_plugin(plugin, plugin_id, transmit):
    """ Reads events from the queue then request data to the plugin and
    stores it back to the data list
    """
    # Check if plugin is outdated
    if plugin_id < data_list[0]:
        transmit = False

    # Update web data and read queue (async ?)
    else:
        # Event pattern
        # event_queue.put({"method":"GET", "data":"refresh"})
        while transmit:
            # Gets the events from the queue
            event = event_queue.get() # Blocking
            plugin.send(json.dumps(event).encode())
            msg("sent data", 0, "Plugin", event)

            # receive data from plugin
            response = plugin.recv(BUFFSIZE).decode()
            msg(response, 3)
            msg("got data", 0, "Plugin", response)

            if response == "EOT": # End of transmission with the plugin
                transmit = False

            else:
                # Update data in data_list and set refresh_flag to True
                data_list[1] = json.loads(response)
                data_list[2] = True



    return transmit


def handle_web_client(web_client, web_client_id, transmit):
    """ This function gets events from the web client and adds them to
    the queue, plugin should handle the events and send back adequate data
    that will then be sent back from here to the client
    """
    # Getting events
    event = json.loads(web_client.recv(BUFFSIZE).decode())
    event_queue.put(event)

    # Send data back if data refresh flag is True
    refreshed = False
    while not refreshed:
        if data_list[2]:
            web_client.send(json.dumps(data_list[1]).encode())
            data_list[2] = False # Put the refresh flag to False again
            refreshed = True

    transmit = False

    # Detect if client is still connected
    return transmit


def handle_client(client, addr, user, client_id):
    global end # Close server
    transmit = True # Close transmission with client

    while transmit:
        if user == "plugin":
            transmit = handle_plugin(client, client_id, transmit)

        elif user == "web_client":
            transmit = handle_web_client(client, client_id, transmit)

    # Message for thread ending
    msg(user + "_" + str(client_id), 2, "Thread", transmit)
    return None


if __name__ == "__main__":
    event_queue = Queue() # All events coming from web clients

    # Html data or forms container [id, data, refresh_flag]
    data_list = [0, "", False]

    try:
        msg("Starting", 1, "Server", server_addr)
        client_id = 0
        while True:
            if not end:
                # Accepting client connection
                client, addr = server.accept()
                user = client.recv(BUFFSIZE).decode() # 1 recv

                # Check if user is a possible name
                if user == "plugin" or user == "web_client":
                    # User accepted
                    client.send(b"a:client_connected") # 1 send

                    # If user is plugin then change id in data_list[0]
                    # This is used to verify plugin
                    if user == "plugin":
                        data_list[0] = client_id
                else:
                    # Bad user
                    client.send(b"e:bad_user")
                    msg("Refused", 2, "Server", user, client_id)

                client_handler = threading.Thread(
                    name=user + "_" + str(client_id),
                    target=handle_client,
                    args=(client, addr, user, client_id),
                    daemon=True
                    )
                msg(client_handler.getName(), 0, "Thread", user, client_id)
                client_handler.start()
                client_id += 1
            else:
                server.close()
                msg("Terminating",  2, "Server")
                break
    except KeyboardInterrupt:
        print()
        # traceback.print_exc()
        msg("Interruption", 3, "Server", server)
        server.close()
