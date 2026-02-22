import os
from fyg.util import cmd, output, confirm, Named

class Installer(Named):
	def __init__(self):
		self.path = os.path.expanduser("~/.local/share/gnome-shell/extensions")
		self.name = "gnomopo@mkult.co"
		self.xpath = "%s/%s"%(self.path, self.name)
		self.epath = "%s/extension.js"%(self.xpath,)
		self.log("initialized")

	def installed(self):
		self.log("looking for", self.epath)
		isinstalled = os.path.exists(self.epath)
		self.log("installed:", isinstalled)
		return isinstalled

	def install(self):
		if not confirm("install extension"):
			return self.log("install declined")
		if not os.path.exists(self.xpath):
			self.log("building", self.xpath)
			cmd("mkdir -p %s"%(self.xpath,))
		for fname in ["extension.js", "metadata.json"]:
			cmd("cp %s %s"%(fname, self.xpath))
		self.log("great, gnomopo is almost ready, but you probably have 2 more steps:")
		self.log("1) restart your gnome session to load the extension")
		self.log("2) run 'gnomopo enable' to enable the extension")

	def uninstall(self):
		if not confirm("uninstall extension"):
			return self.log("uninstall declined")
		cmd("rm -rf %s"%(self.xpath,))

	def enabled(self):
		info = output("gnome-extensions info %s"%(self.name,), loud=True)
		return "Enabled: Yes" in info

	def enable(self):
		if self.enabled():
			return self.log("already enabled!")
		if not confirm("enable extension"):
			return self.log("enable declined")
		cmd("gnome-extensions enable %s"%(self.name,))

	def disable(self):
		if not self.enabled():
			return self.log("already disabled!")
		if not confirm("disable extension"):
			return self.log("disable declined")
		cmd("gnome-extensions disable %s"%(self.name,))

	def status(self):
		if self.installed():
			enabled = self.enabled()
			self.log("enabled:", enabled)
			current = not output("diff extension.js %s"%(self.epath,), loud=True)
			self.log("current:", current)
			current or self.log('type "gnomopo reinstall" to update the extension')
			enabled or self.log('type "gnomopo enable" to enable the extension')

	def run(self, action="install"):
		self.log("run", action)
		if action == "status":
			self.status()
		elif action.endswith("able"):
			getattr(self, action)()
		else: # install, uninstall, reinstall
			if action in ["uninstall", "reinstall"]:
				self.uninstall()
			if action != "uninstall":
				if self.installed():
					self.log("already installed! don't forget to enable!")
				else:
					self.install()
		self.log("goodbye")