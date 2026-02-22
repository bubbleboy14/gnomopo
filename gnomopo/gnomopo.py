import os
from optparse import OptionParser
from fyg.util import confirm, cmd
from .util import setverbosity, log, getres
from .installer import Installer

def getpos(withmods=False, addr="127.0.0.1", port=62090):
	res = getres("mpos", addr, port)
	return res if withmods else res[:2]

def getsize(withscale=True, addr="127.0.0.1", port=62090):
	res = getres("size", addr, port)
	return res if withscale else res[:2]

def getwindow(rect="both", addr="127.0.0.1", port=62090):
	res = getres("window", addr, port)
	return res if rect == "both" else res[rect] # frame or buffer

def invoke():
	parser = OptionParser("gnomopo [getpos|getsize|getwindow|status|enable|disable|install|reinstall|uninstall] -v")
	parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
		default=False, help="a few extra getpos/getsize logs")
	ops, args = parser.parse_args()
	action = args and args[0]
	setverbosity(ops.verbose)
	if action == "status" or action.endswith("install") or action.endswith("able"):
		os.chdir(os.path.abspath(__file__).rsplit("/", 1).pop(0))
		Installer().run(action)
	elif action == "getpos":
		print(*getpos())
	elif action == "getsize":
		print(*getsize())
	elif action == "getwindow":
		print(getwindow())

if __name__ == "__main__":
	invoke()