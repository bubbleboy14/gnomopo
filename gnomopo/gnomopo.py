import os
from optparse import OptionParser
from fyg.util import confirm, cmd
from .util import setverbosity, log, getres
from .installer import Installer

def getpos(addr="127.0.0.1", port=62090):
	return getres("pos", addr, port)

def getsize(addr="127.0.0.1", port=62090):
	return getres("size", addr, port)

def invoke():
	parser = OptionParser("gnomopo [getpos|getsize|install|reinstall|uninstall] -v")
	parser.add_option("-v", "--verbose", action="store_true",
		dest="verbose", default=False, help="log stuff")
	ops, args = parser.parse_args()
	action = args and args[0]
	setverbosity(ops.verbose)
	if action.endswith("install"):
		os.chdir(os.path.abspath(__file__).rsplit("/", 1).pop(0))
		Installer().run(action)
	else:
		if action == "getpos":
			print(*getpos())
		elif action == "getsize":
			print(*getsize())

if __name__ == "__main__":
	invoke()