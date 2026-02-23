import socket, json, atexit
from fyg.util import basiclog

SOCK = None
VERBOSE = False
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
		SOCK = None

def send(msg, addr="127.0.0.1", port=62090):
	dosend = lambda : getsock(addr, port).send(msg.encode() + b"\n")
	try:
		dosend()
	except:
		log("send error - reconnecting")
		closesock()
		dosend()

atexit.register(closesock)

def getres(action="mpos", addr="127.0.0.1", port=62090):
	try:
		send(action, addr, port)
		resp = getsock(addr, port).recv(128).decode()
		if action == "window":
			coords = json.loads(resp)
		else:
			coords = [int(v) for v in resp.split(" ")]
		log("getres", action, coords)
		return coords
	except Exception as e:
		log("getres", action, "failed:", e)