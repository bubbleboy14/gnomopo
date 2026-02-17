import os, socket
from optparse import OptionParser
from fyg.util import confirm, basiclog, cmd

VERBOSE = True
def setverbosity(isverb):
	global VERBOSE
	VERBOSE = isverb

def log(*msg):
	VERBOSE and basiclog("gnomopo:", *msg)

def getpos(addr='127.0.0.1', port=62090):
	try:
		sock = socket.create_connection((addr, port))
		pos = sock.recv(16).decode()
		coords = [int(v) for v in pos.split(" ")]
		log(coords)
		return coords
	except:
		log("getpos failed")

def install():
	log("checking for installation...")
	fpath = "~/.local/share/gnome-shell/extensions"
	ename = "gnomopo@mkult.co"
	xpath = "%s/%s"%(fpath, ename)
	epath = "%s/extension.js"%(xpath,)
	if os.path.exists(epath):
		log("found", epath)
		if confirm("enable extension?"):
			cmd("gnome-extensions enable %s"%(ename,))
		log("great, you're probably good to go!")
	else:
		log("can't find", epath)
		if confirm("install extension"):
			if not os.path.exists(xpath):
				log("building", xpath)
				cmd("mkdir -p %s"%(xpath,))
			for fname in ["extension.js", "metadata.json"]:
				cmd("cp %s %s"%(fname, xpath))
			log("great, gnomopo is almost ready - 2 more steps:")
			log("1) restart your gnome session")
			log("2) run 'gnomopo install' again to enable the extension")

def invoke():
	parser = OptionParser("gnomopo [getpos|install] -v")
	parser.add_option("-v", "--verbose", action="store_true",
		dest="verbose", default=False, help="log stuff")
	ops, args = parser.parse_args()
	setverbosity(ops.verbose)
	if args and args[0] == "install":
		install()
	else:
		print(*getpos())

if __name__ == "__main__":
	invoke()