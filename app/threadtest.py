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

import threading

counter = 0

def increment():
	global counter
	for _ in range(100_000):
		#with lock:
		counter += 1

threads = [threading.Thread(target=increment) for _ in range(5)]
for t in threads: t.start()
for t in threads: t.join()

print(counter)  # always 500000