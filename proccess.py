import subprocess
import os

class Proccess:

	def __init__(self, name, data):
		self.name = name
		self.command = data["command"]
		if "stdout" in data:
			f = open(data["stdout"])
			self.stdout = f
		else:
			self.stdout = None
		self.proccess = None
		self.pid = None

	def start(self):
		self.proccess = subprocess.Popen(
			self.command.split(" "),
			shell = True, env = os.environ,
			stdin = subprocess.PIPE,
			stdout = self.stdout);
		self.pid = self.proccess.pid

	def status(self):
		print "name ->"+self.name+" pid->"+ self.pid