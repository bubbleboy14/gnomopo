import os, socket
from fyg.util import confirm, basiclog, cmd

def log(*msg):
	basiclog("gnomopo:", *msg)

def getpos(addr='127.0.0.1', port=62090):
	try:
		sock = socket.create_connection((addr, port))
		pos = sock.recv(16)
		log("getpos", pos)
		return [int(v) for v in pos.decode().split(" ")]
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
			log("2) run gnomopo again to enable the extension")

if __name__ == "__main__":
	install()