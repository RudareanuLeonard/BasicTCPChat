import threading
import socket

host = '127.0.0.1'
port = 5007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()

clients = [] #list of clients
nicknames = [] #list of nicknames

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client_connection(client):
    while True:
        try:
            received_message = client.recv(50) # we receive the message from the client
            broadcast(received_message) #we share the message with the others
        except:
            index_of_the_client = clients.index(client) # we get the index of the client so we can delet it later
            clients.remove(client)
            nickname = nicknames[index_of_the_client]
            nicknames.remove(nickname)
            client.close() # we close the connection of the client to the server
            broadcast(f"{nickname} left the chat".encode("utf-8"))
            break
    

def receive():
    while True:
        client, adress = s.accept()
        print(f"connected with {str(adress)}")
        client.send("Pick a nickname".encode('utf-8'))
        nickname = client.recv(50).decode("utf-8")
        clients.append(client)
        nicknames.append(nickname)

        print(f"{str(nickname)} is here")

        # broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        broadcast("{} joined!".format(nickname).encode("ascii"))
        thread = threading.Thread(target=handle_client_connection, args=(client,))
        thread.start()



print("server is OK")

receive()