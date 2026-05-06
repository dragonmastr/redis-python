import threading, time

# def fetch(url):
# 	time.sleep(1)
# 	print(f"Fetched: {url}")

# urls = ["api/users", "api/orders", "api/products"]

# threads = [threading.Thread(target=fetch, args=(u,)) for u in urls]
# print(threads)

# for t in threads:
# 	t.start()

# for t in threads:
# 	t.join()  # wait for ALL threads

# print("All done")

# import threading

# counter = 0

# def increment():
# 	global counter
# 	for _ in range(100_000):
# 		#with lock:
# 		counter += 1

# threads = [threading.Thread(target=increment) for _ in range(5)]
# for t in threads: t.start()
# for t in threads: t.join()

# print(counter)  # always 500000

def parse_resp(data):
    parts = data.split("\r\n")
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
        
        


parse_resp("*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n")