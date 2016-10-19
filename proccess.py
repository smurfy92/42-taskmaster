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
			self.stdout = data["stdout"]
		else:
			self.stdout = None
		if "stderr" in data:
			self.stderr = data["stderr"]
		else:
			self.stderr = None
		self.proccess = None
		self.pid = None
		self.statuss = "STOPPED"
		self.starttime = None
		self.rc = None
		self.startednb = 0
		if "umask" in data:
			self.umask = data["umask"]
		else:
			self.umask = 022
		if "returncodes" in data:
			self.returncodes = data["returncodes"]
		else:
			self.returncodes = None
		if "signal" in data:
			self.signal = data["signal"]
		else:
			self.signal = None
		if "running" in data:
			self.running = data["running"]
		else:
			self.running = 0
		if "restart" in data:
			self.restart = data["restart"]
		else:
			self.restart = None
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
		if "workingdir" in data:
			self.workingdir = data["workingdir"]
		else:
			self.workingdir = None
		if "autostart" in data:
			self.start()



	def start(self, init=0):
		if init == 0:
			print "Started : "+self.name
		try:
			oldmask = os.umask(self.umask)
			if self.stdout != None:
				stdout = open(self.stdout, "a+")
			else:
				stderr = None
			if self.stderr != None:
				stderr = open(self.stderr, "a+")
			else:
				stderr = None
			self.proccess = subprocess.Popen(
				self.command,
				shell = True,
				env = os.environ,
				stdin = subprocess.PIPE,
				stdout = stdout,
				stderr = stderr);
			os.umask(oldmask)
			self.pid = self.proccess.pid
			self.startednb += 1
			if (self.running > 0):
				self.statuss = "STARTING"
			else:
				self.statuss = "RUNNING"
			self.starttime = time.time()
			log.info(" started : "+self.name + " uptime : "+time.strftime("%H:%M:%S", time.gmtime(self.starttime)))
		except Exception, e:
			log.warning("failed to launch"+self.name + ': ' + str(e))
			print "failed to launch "+self.name+ " error : "+ str(e)

	def status(self):
		if (self.statuss == "RUNNING" or self.statuss == "STARTING"):
			timer = time.time()
			time_delta = time.gmtime(timer - self.starttime)
			curr_time = time.strftime("%H:%M:%S", time_delta)
			print ("NAME : {0} | STATUS : {1} | PID : {2} | UPTIME :"+ curr_time).format(self.name, self.statuss, str(self.pid))
		else:
			print "NAME : "+self.name+"| STATUS : "+self.statuss

	def stop(self):
		print "Stopped : "+self.name
		log.info(" stopped : "+ self.name)
		if self.signal:
			try:
				self.proccess.send_signal(self.signal)
			except Exception, e:
				log.error(self.name+" signal not permitted")
				print self.name +" signal not working"
		else:
			self.proccess.terminate()
		self.pid = None
		self.statuss = "STOPPED"
		self.starttime = None

	def check(self):
		if self.proccess.poll() != None:
			self.rc = self.proccess.poll()
			self.pid = None
			self.statuss = "STOPPED"
			self.starttime = None
			if self.restart == "always" or self.restartnb >= self.startednb:
				self.start()
			if self.restart == "unexpected" and self.rc not in self.returncodes:
				self.start()
		elif self.running > 0:
			if time.time() - self.starttime >= self.running:
				self.statuss = "RUNNING"