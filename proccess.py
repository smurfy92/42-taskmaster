import subprocess
import os
import time
import logging

log = logging
log.basicConfig(filename = '/tmp/taskmaster.log', level=logging.DEBUG)

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
		self.statuss = "STOPPED"
		self.starttime = None
		if "autostart" in data:
			self.start()

	def start(self):
		self.proccess = subprocess.Popen(
			self.command.split(" "),
			shell = True, env = os.environ,
			stdin = subprocess.PIPE,
			stdout = self.stdout);
		self.pid = self.proccess.pid
		self.statuss = "RUNNING"
		self.starttime = time.time()
		log.info("started :"+self.name + "time :"+time.strftime("uptime: %H:%M:%S", time.gmtime(self.starttime)))
		#self.check()

	def status(self):
		if (self.statuss == "RUNNING"):
			timer = time.time()
			time_delta = time.gmtime(timer - self.starttime)
			curr_time = time.strftime("uptime: %H:%M:%S", time_delta)

			self.name = "%10s" % self.name
			print ("NAME : {0}| STATUS : "+self.statuss+" | PID : "+ str(self.pid)+"| STARTTIME :"+ curr_time).format(self.name)
		else:
			print "NAME : "+self.name+"| STATUS : "+self.statuss

	def check(self):
		print "check"