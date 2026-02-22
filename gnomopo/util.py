import socket, json
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

