import subprocess
import os
import time
import logging
import shlex

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
		if "stderr" in data:
			f = open(data["stderr"],"a+")
			self.stderr = f
		else:
			self.stderr = None
		self.proccess = None
		self.pid = None
		self.statuss = "STOPPED"
		self.starttime = None
		if "restart" in data:
			self.restart = data["restart"]
		if "expected" in data:
			self.expected = data["expected"]
		if "exitcodes" in data:
			self.exitcodes = data["exitcodes"]
		if "restartnb" in data:
			self.restartnb = data["restartnb"]
		else:
			self.restartnb = 0
		if "signal" in data:
			self.signal = data["signal"]
		if "timetoexit" in data:
			self.timetoexit = data["timetoexit"]
		if "autostart" in data:
			self.start(init=1)



	def start(self, init=0):
		if init == 0:
			print "Started : "+self.name
		self.proccess = subprocess.Popen(
			self.command,
			shell = True,
			env = os.environ,
			stdin = subprocess.PIPE,
			stdout = self.stdout,
			stderr = self.stderr);
		self.pid = self.proccess.pid
		self.statuss = "RUNNING"
		self.starttime = time.time()
		log.info(" started : "+self.name + " uptime : "+time.strftime("%H:%M:%S", time.gmtime(self.starttime)))

	def status(self):
		if (self.statuss == "RUNNING"):
			timer = time.time()
			time_delta = time.gmtime(timer - self.starttime)
			curr_time = time.strftime("%H:%M:%S", time_delta)
			print ("NAME : {0} | STATUS : {1} | PID : {2} | UPTIME :"+ curr_time).format(self.name, self.statuss, str(self.pid))
		else:
			print "NAME : "+self.name+"| STATUS : "+self.statuss

	def stop(self):
		print "Stopped : "+self.name
		log.info(" stopped : "+ self.name)
		self.proccess.terminate()
		self.pid = None
		self.statuss = "STOPPED"
		self.starttime = None

	def check(self):
		print "check"