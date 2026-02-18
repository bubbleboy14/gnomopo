import socket
from fyg.util import basiclog

VERBOSE = False
def setverbosity(isverb):
	global VERBOSE
	VERBOSE = isverb

def log(*msg):
	VERBOSE and basiclog("gnomopo:", *msg)

def getres(action="mpos", addr="127.0.0.1", port=62090):
	try:
		sock = socket.create_connection((addr, port))
		sock.write(action.encode())
		resp = sock.recv(16).decode()
		coords = [int(v) for v in resp.split(" ")]
		log("getres", action, coords)
		return coords
	except:
		log("getres", action, "failed")

