import socket  # noqa: F401
import threading

def handle_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        connection.sendall(b"+PONG\r\n")

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, _ = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client,args=(connection,), daemon=True)
        thread.start()



if __name__ == "__main__":
    main()
