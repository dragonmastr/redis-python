import socket  # noqa: F401
import threading
import time

kv = {}
def handle_client(connection):
    while True:
        data = connection.recv(1024)
        if not data:
            break
        try:
            parsed = parse_resp(data)
        except Exception as e:
            print("Parser Error:", e)
            continue
        command = parsed[0].upper()
        if command == "PING":
            connection.sendall(b"+PONG\r\n")

        elif command == "ECHO":
            message = parsed[1]
            response = f"${len(message)}\r\n{message}\r\n"
            connection.sendall(response.encode())

        elif command == "SET":
            key = parsed[1]
            value = parsed[2]

            entry = {
                "value": value,
                "expiry": None
            }
            if len(parsed) > 3:
                expiry_type = parsed[3].upper()
                current_time = time.time()
                expiry_time = int(parsed[4])
                if expiry_type == "EX":
                    entry["expiry"] = expiry_time + current_time
                elif expiry_type == "PX":
                    entry["expiry"] = expiry_time/1000 + current_time
            # we are storing the key value pair such that we have expiry in place
            kv[key] = entry
            connection.sendall(b"+OK\r\n")

        elif command == "GET":
            key = parsed[1]
            if key in kv:
                current_time = time.time()
                expiry_time = kv[key]["expiry"] 
                if expiry_time is None:
                    value = kv[key]["value"]
                    response = f"${len(value)}\r\n{value}\r\n"
                    connection.sendall(response.encode())
                if current_time > expiry_time:
                    del kv[key]
                    connection.sendall(b"$-1\r\n")
                value = kv[key]["value"]
                response = f"${len(value)}\r\n{value}\r\n"
                connection.sendall(response.encode())
            else:
                connection.sendall(b"$-1\r\n")
        
        elif command == "RPUSH":
            listname = parsed[1]
            value = parsed[2:]
            if listname not in kv:
                kv[listname] = []
            print(listname)
            for v in value:
                kv[listname].append(v) 
            length = len(kv[listname])
            response = f":{length}\r\n"
            connection.sendall(response.encode())
                


def parse_resp(data):
    parts = data.decode().split("\r\n")
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
