import threading
import socket

nickname = input("Enter a nickname: ")
print(nickname)

host = '127.0.0.1'
port = 5007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def receive():
    while True:
        try:
            message = s.recv(50).decode("utf-8")
            if message == "Pick a nickname":
                s.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print("CLIENT CLOSED")
            s.close()
            break

def write():
    while True:
        message = f'{nickname}: {input("")}'
        s.send(message.encode("utf-8"))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()