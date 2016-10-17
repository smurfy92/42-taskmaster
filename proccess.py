import subprocess
import os

class Proccess:

	def __init__(self, name, data):
		self.name = name
		self.command = data["command"]
		if "stdout" in data:
			f = open(data["stdout"],"a+")
			self.stdout = f
		else:
			self.stdout = None
		self.proccess = None
		self.pid = None


		if "autostart" in data:
			self.start()

	def start(self):
		self.proccess = subprocess.Popen(
			self.command.split(" "),
			shell = True, env = os.environ,
			stdin = subprocess.PIPE,
			stdout = self.stdout);
		self.pid = self.proccess.pid
		self.check()

	def status(self):
		if (self.pid):
			print "NAME : "+self.name+" | PID : "+ str(self.pid)

	def check(self):
		print "check"