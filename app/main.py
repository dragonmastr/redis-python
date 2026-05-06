import socket  # noqa: F401
import threading

def handle_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        parsed = parse_resp(data)
        command = parsed[0].upper()
        if command == "PING":
            connection.sendall(b"+PONG\r\n")
        elif command == "ECHO":
            message = parsed[1]
            response = f"${len(message)}\r\n{message}\r\n"
            connection.sendall(response.encode())

def parse_resp(data):
    parts = data.decode().split("\r\n")
    print(parts)
    if not parts[0].startswith("*"):
        raise ValueError("Invalid RESP Array")
    element_count = int(parts[0][1:])
    result = []
    index = 1
    for _ in range(element_count):
        if not parts[index].startswith("$"):
            raise ValueError("Expected Bulk String")
        length = int(parts[index][1:])
        value = parts[index+1]
        if len(value) != length:
            raise ValueError("Invalid Bulk String Length")
        result.append(value)
        index += 2
        
    return result


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        connection, _ = server_socket.accept() # wait for client
        thread = threading.Thread(target=handle_client,args=(connection,), daemon=True)
        thread.start()



if __name__ == "__main__":
    main()
