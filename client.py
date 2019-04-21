import socket
import time
import json

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
client.settimeout(0.2)
#client.bind(("0.0.0.0", 44444))
message = {"coin":"simplecoin"}

knownlist = []

while True:
    new = json.dumps(message)
    client.sendto(new.encode(), ('<broadcast>', 5001))
    print("message sent!")
    time.sleep(1)