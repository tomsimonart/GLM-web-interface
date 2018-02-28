#!/usr/bin/env python3

import json
import socket
import threading
from GLM import glm
from sys import argv
from time import sleep
from queue import Queue
import multiprocessing
from GLM.source.libs.rainbow import msg
import traceback

BUFFSIZE = 512
end = False

addr = "localhost"
port = 9999

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

if len(argv) >= 2 and argv[1].isdecimal():
    port = int(argv[1])

server_addr = (addr, port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Re-use port
server.bind(server_addr)
server.listen(5)

# All events coming from web clients
event_queue = Queue()
# Html data or forms container [id, data, refresh_flag_int]
data_list = [0, "", 0]

plugin_loader_queue = multiprocessing.Queue()


def handle_plugin(plugin, plugin_id, transmit):
    """ Reads events from the queue then request data to the plugin and
    stores it back to the data list
    """
    client.send(b"a:client_connected")
    while transmit:
        status = plugin.recv(BUFFSIZE).decode()

        # event_queue get REFRESH

        # event_queue get DICT type

    # while transmit:
    #     # Check if plugin is outdated
    #     if plugin_id < data_list[0]:
    #         transmit = False
    #
    #     status = plugin.recv(BUFFSIZE).decode()
    #
    #     if status == "READY":
    #         # Gets the events from the queue
    #         event = event_queue.get() # Blocking
    #         plugin.send(json.dumps(event).encode())
    #         msg("sent data", 0, "Plugin", event)
    #
    #         # receive data from plugin
    #         response = plugin.recv(BUFFSIZE).decode()
    #         msg("got data", 0, "Plugin", response)
    #
    #         # End of transmission with the plugin
    #         if response == "EOT" or response == "":
    #             transmit = False
    #
    #         else:
    #             # Update data in data_list and set refresh_flag to True
    #             msg(response)
    #             print(plugin)
    #             msg(json.loads(response), 3)
    #             data_list[1] = json.loads(response)
    #             data_list[2] += 1
    #
    #     elif status == "EOT" or status == "":
    #         transmit = False
    #
    #     else:
    #         transmit = False
    #
    # return transmit


def handle_web_client(web_client, web_client_id, transmit, plugin_loader):
    """ This function should be able to receive events from clients and
    execute actions like (spawning a plugin process, sending web data back...)
    """
    client.send(b"a:client_connected")

    while transmit:

        # Add event to queue
        event = web_client.recv(BUFFSIZE).decode()
        if not event or event == "EOT":
            transmit = False

        else:
            event_read = json.loads(event)

            # Plugin loading phase
            event_test = event_read.pop("LOADPLUGIN", None)
            if event_test is not None:
                msg("Plugin phase", 1, "web_client_handler", web_client_id)
                if plugin_loader is not None:
                    plugin_loader_queue.put("END")
                    plugin_loader_queue.join() # Wait for process to end
                plugin_loader = multiprocessing.Process(
                    target=glm.plugin_loader,
                    daemon=False,
                    args=(
                        glm.plugin_scan(PLUGIN_DIRECTORY)[event_test], # id
                        plugin_loader_queue,
                        True, # start
                        False, # matrix
                        True, # show
                        False # guishow
                        )
                    )
                plugin_loader.start()
                msg("plugin loaded", 0, "Status")
                web_client.send(b"status:plugin_loaded")

            # Getting data phase
            event_test = event_read.pop("READ", None)
            if event_test is not None:
                msg("Getting data phase", 1, "web_client_handler", web_client_id)
                if event_test == "REFRESH":
                    # TODO web_client.send(data_list[1].encode())
                    data_state = data_list[2]
                    event_queue.put(event_test)
                    while data_state >= data_list[2]:
                        # Event is waiting for refresh
                        sleep(0.2)
                    web_client.send(data_list[1].encode())

            # Sending events phase
            event_test = event_read.pop("WRITE", None)
            if event_test is not None:
                msg("Sending events phase", 1, "web_client_handler", web_client_id)
                event_queue.put(event_test)
                web_client.send("status:got_event")

    return transmit


def handle_client(client, addr, user, client_id):
    global end # Close server
    transmit = True # Close transmission with client

    while transmit:
        if user == "plugin":
            transmit = handle_plugin(client, client_id, transmit)

        elif user == "web_client":
            transmit = handle_web_client(
                client,
                client_id,
                transmit,
                plugin_loader
                )

    # Message for thread ending
    msg(user + "_" + str(client_id), 2, "Thread", transmit)
    return None


if __name__ == "__main__":
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
        traceback.print_exc()
        msg("Interruption", 3, "Server", server)
        server.close()
