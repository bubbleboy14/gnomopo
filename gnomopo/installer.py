import os
from fyg.util import cmd, confirm, Loggy

class Installer(Loggy):
	def run(self, variant="install"):
		self.log("checking for installation...")
		fpath = "~/.local/share/gnome-shell/extensions"
		ename = "gnomopo@mkult.co"
		xpath = "%s/%s"%(fpath, ename)
		epath = "%s/extension.js"%(xpath,)
		if os.path.exists(epath):
			self.log("found", epath)
			if confirm("enable extension?"):
				cmd("gnome-extensions enable %s"%(ename,))
			self.log("great, you're probably good to go!")
		else:
			self.log("can't find", epath)
			if confirm("install extension"):
				if not os.path.exists(xpath):
					self.log("building", xpath)
					cmd("mkdir -p %s"%(xpath,))
				for fname in ["extension.js", "metadata.json"]:
					cmd("cp %s %s"%(fname, xpath))
				self.log("great, gnomopo is almost ready - 2 more steps:")
				self.log("1) restart your gnome session")
				self.log("2) run 'gnomopo install' again to enable the extension")
