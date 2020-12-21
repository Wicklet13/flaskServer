import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "108.49.176.195"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))

connected = True

while connected:
    message = input("Input your message: \n")
    send(message)
    print("\n")
    if (client.recv(HEADER).decode(FORMAT) == 'Disconnected'):
        connected = False