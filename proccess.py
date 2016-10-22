import subprocess
import os
import time
import logging

log = logging
log.basicConfig(filename = '/tmp/taskmaster.log', level=logging.DEBUG)

def killslowlybutsurely(p, time):
	if p.proccess.poll() != None:
		sleep(time)
		p.proccess.terminate()

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
		if "gracefullstop" in data:
			self.gracefullstop = data["gracefullstop"]
		else:
			self.gracefullstop = None
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
		if "workingdir" in data:
			self.workingdir = data["workingdir"]
		else:
			self.workingdir = None
		env = os.environ.copy()
		if "env" in data:
			for p in data["env"]:
				env[p] = data["env"][p]
			self.env = env
		else:
			self.env = None
		if "autostart" in data:
			self.start(1)

	def start(self, init=0):
		if init == 0:
			print "Started : "+self.name
		oldmask = os.umask(self.umask)
		if self.stdout != None:
			stdout = open(self.stdout, "w+")
		else:
			stdout = None
		if self.stderr != None:
			stderr = open(self.stderr, "w+")
		else:
			stderr = None
		os.umask(oldmask)
		try:
			self.proccess = subprocess.Popen(
				self.command,
				cwd = self.workingdir,
				shell = True,
				stdin = subprocess.PIPE,
				stdout = stdout,
				stderr = stderr,
				env = self.env);
			self.pid = self.proccess.pid
			self.startednb += 1
			if (self.running > 0):
				self.statuss = "STARTING"
			else:
				self.statuss = "RUNNING"
			self.starttime = time.time() + 7200
			log.info(" started : "+self.name + " uptime : "+time.strftime("%H:%M:%S", time.gmtime(self.starttime)))
		except Exception, e:
			log.warning("failed to launch"+self.name + ': ' + str(e))
			print "failed to launch "+self.name+ " error : "+ str(e)

	def status(self):
		if (self.statuss == "RUNNING" or self.statuss == "STARTING"):
			timer = time.time() + 7200
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
				print self.name +" signal not permitted"
				th = threading.Thread(target=killslowlybutsurely)
				th.daemon = True
				th.start()
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
				self.start(1)
			if self.restart == "unexpected" and self.rc not in self.returncodes:
				self.start(1)
		elif self.running > 0 and self.starttime:
			if (time.time() + 7200) - self.starttime >= self.running:
				self.statuss = "RUNNING"