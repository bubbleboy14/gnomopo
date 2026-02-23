import socket, json, atexit
from fyg.util import basiclog

SOCK = None
VERBOSE = True
def setverbosity(isverb):
	global VERBOSE
	VERBOSE = isverb

def log(*msg):
	VERBOSE and basiclog("gnomopo:", *msg)

def getsock(addr="127.0.0.1", port=62090):
	global SOCK
	if not SOCK:
		log("connecting")
		SOCK = socket.create_connection((addr, port))
	return SOCK

def closesock():
	global SOCK
	if SOCK:
		log("disconnecting")
		SOCK.close()

atexit.register(closesock)

def getres(action="mpos", addr="127.0.0.1", port=62090):
	try:
		sock = getsock(addr, port)
		sock.send(action.encode() + b"\n")
		resp = sock.recv(128).decode()
		if action == "window":
			coords = json.loads(resp)
		else:
			coords = [int(v) for v in resp.split(" ")]
		log("getres", action, coords)
		return coords
	except Exception as e:
		log("getres", action, "failed:", e)