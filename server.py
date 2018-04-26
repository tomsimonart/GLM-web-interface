#!/usr/bin/env python3

import json
import socket
import argparse
import threading
import traceback
import multiprocessing
from os import path
from GLM import glm
from sys import argv
from time import sleep
from queue import Queue, Empty
from GLM.source.libs.rainbow import msg

BUFFSIZE = 512
end = False

glm.PLUGIN_PACKAGE = "GLM.source.plugins"
PLUGIN_DIRECTORY = "./GLM/source/" + glm.PLUGIN_PREFIX + "/"
plugin_loader = None

parser = argparse.ArgumentParser(description="Serve GLM")
parser.add_argument('--host', help='Host', default='localhost', type=str)
parser.add_argument('--port', '-p', help='Port', default=9999, type=int)
parser.add_argument('--verbose', '-v', action='count', help='Verbose level', default=0)
parser.add_argument('--sverbose', '-V', help='Special verbosity', action='append', type=str)
parser.add_argument('--matrix', '-m', help='Matrix enabled', action='store_true')
parser.add_argument('--show', '-s', help='Virtual matrix enabled',
action='store_true')
parser.add_argument('--guishow', '-g', help='GUI enabled', action='store_true')

args = parser.parse_args()

dir = path.dirname(__file__)
rel_path = path.join(dir, 'GLM/verbosity')

with open(rel_path, 'w') as f:
    f.write(str(args.verbose)+'\n')
    if args.sverbose is not None:
        for arg in args.sverbose:
            f.write(arg+'\n')
clients = {}


# if len(argv) >= 2 and argv[1].isdecimal():
#     port = int(argv[1])

server_addr = (args.host, args.port)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Re-use port
server.bind(server_addr)
server.listen(0)

# All events coming from web clients
event_queue = Queue()
# Html data or forms container [id, data, refresh_count]
data_list = [0, "", 0, 0]
current_plugin_id = []

plugin_loader_queue = multiprocessing.Queue()


def handle_plugin(plugin, plugin_id, transmit):
    """ Reads events from the queue then request data to the plugin and
    stores it back to the data list
    """
    client.send(b"a:client_connected")
    while transmit:
        response = plugin.recv(BUFFSIZE).decode()
        if not response or response == "EOT": # Single receive
            transmit = False

        elif response == "READY":
            try:
                event = event_queue.get() # Waiting for event
            except Empty:
                event = None
            else:
                pass

            msg(str(response), 3, 'response') # Debug
            # refresh phase
            if event == "REFRESH":
                plugin.send(json.dumps(event).encode())
                data_json = plugin.recv(BUFFSIZE).decode()
                if not data_json or data_json == "EOT":
                    transmit = False
                else:
                    data = json.loads(data_json)
                    data_list[2] += 1
                    data_list[1] = data
                plugin.send(b'ok')
                # except BrokenPipeError:
                #     transmit = False
                #     plugin.close()
                #     msg('pipe broken', 1, level=0)
                #     return transmit

            if event == "UPDATE":
                plugin.send(json.dumps(event).encode())
                data_json = plugin.recv(BUFFSIZE).decode()
                if not data_json or data_json == "EOT":
                    transmit = False
                else:
                    data = json.loads(data_json)
                    data_list[3] = data
                plugin.send(b'ok')
                # except BrokenPipeError:
                #     transmit = False
                #     plugin.close()
                #     msg('pipe broken', 1, level=0)
                #     return transmit

            # event phase
            elif type(event) == dict:
                plugin.send(json.dumps(event).encode())
                status = plugin.recv(BUFFSIZE).decode()
                if not status or status == "EOT":
                    transmit = False
                elif status == "RECEIVED":
                    # Event received
                    pass
                plugin.send(b'ok')
                # except BrokenPipeError:
                #     transmit = False
                #     plugin.close()
                #     msg('pipe broken', 1, level=0)
                #     return transmit

            # Reset event !!!
            event = None

    plugin.close()
    return transmit


def handle_web_client(web_client, web_client_id, transmit):
    """ This function should be able to receive events from clients and
    execute actions like (spawning a plugin process, sending web data back...)
    """
    global plugin_loader
    client.send(b"a:client_connected")

    while transmit:

        # Add event to queue
        event = web_client.recv(BUFFSIZE).decode()
        if not event or event == "EOT":
            transmit = False

        else:
            event_read = json.loads(event)

            # Check if plugin is loaded phase
            event_test = event_read.pop("CHECK", None)
            if event_test is not None:
                if plugin_loader is not None:
                    web_client.send(str(current_plugin_id[0]).encode())
                else:
                    web_client.send(b'None')


            # Plugin loading phase
            event_test = event_read.pop("LOADPLUGIN", None)
            if event_test is not None:
                current_plugin_id.clear()
                current_plugin_id.append(event_test)
                if plugin_loader is not None:
                    while not plugin_loader_queue.empty():
                        print(plugin_loader_queue.qsize()) # Debug
                        sleep(0.05)
                    plugin_loader_queue.put("END")
                    # while not plugin_loader_queue.empty():
                    #     print(plugin_loader_queue.qsize()) # Debug
                    #     sleep(0.05)
                    # ready = plugin_loader_queue.get()
                    plugin_loader.join()
                    # while not plugin_loader_queue.empty():
                    #     msg('plugin running', 1, 'LOADPLUGIN', level=2)
                    #     sleep(0.05)
                plugin_loader = multiprocessing.Process(
                    target=glm.plugin_loader,
                    daemon=False,
                    args=(
                        glm.plugin_scan(PLUGIN_DIRECTORY)[event_test], # id
                        plugin_loader_queue,
                        True, # start
                        args.matrix, # matrix
                        args.show, # show
                        args.guishow # guishow
                        )
                    )
                data_list[3] = 0
                plugin_loader.start()
                web_client.send(b"status:plugin_loaded")

            # Getting data phase
            event_test = event_read.pop("READ", None)
            if event_test is not None:
                if event_test == "REFRESH":
                    data_state = data_list[2]
                    event_queue.put(event_test)
                    while data_state == data_list[2]:
                        # Event is waiting for refresh
                        sleep(0.01)
                        pass

                    web_client.send(json.dumps(data_list[1]).encode())

                # Sending update
                elif event_test == "UPDATE":
                    event_queue.put(event_test)
                    web_client.send(json.dumps(data_list[3]).encode())

            # Sending events phase
            event_test = event_read.pop("WRITE", None)
            if event_test is not None:
                msg("Sending events phase", 1, "web_client_handler", web_client_id, level=2)
                event_queue.put(event_test)
                web_client.send(b"status:got_event")

    web_client.close()
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
                transmit
                )

    # Message for thread ending
    msg(user + "_" + str(client_id), 2, "Thread", transmit, level=3)
    return None


if __name__ == "__main__":
    try:
        msg("Starting", 1, "Server", server_addr, level=1)
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

                    client_handler = threading.Thread(
                    name=user + "_" + str(client_id),
                    target=handle_client,
                    args=(client, addr, user, client_id),
                    daemon=True
                    )
                    msg(client_handler.getName(), 0, "Thread", user, client_id, level=3)
                    client_handler.start()
                    client_id += 1

                else:
                    # Bad user
                    client.send(b"e:bad_user")
                    msg("Refused", 2, "Server", user, client_id, level=0)

            else:
                server.close()
                msg("Terminating",  2, "Server", level=1) # Ending server thread
                break
    except KeyboardInterrupt:
        print()
        with open(rel_path, 'w') as f:
            f.write('1\n')
        msg("Interruption", 3, "Server", server, level=1)
        server.close()
