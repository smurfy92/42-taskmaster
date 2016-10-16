import cmd
from yaml import load, dump
from proccess import *

proc = {}
tab = {}

def init():
    print "Hello world"
    with open('test.conf', 'r') as f:
        doc = load(f)
    for proc in doc:
        tab[proc] = Proccess(proc, doc[proc])

class Prompt(cmd.Cmd):
    """Simple command processor example."""
    prompt = "\033[92mTaskmaster -> \033[0m"

    def do_start(self, line):
        t = line.split(" ")
        if (tab[t[0]]):
            tab[t[0]].start()

    def do_stop(self, line):
    	tab = line.split(" ")
        if (tab[0]):
            proc[tab[0]].terminate()
        print tab

    def do_status(self, line):
        tab = line.split(" ")
        for p in tab:
            p.status

    def do_reload(self, line):
    	tab = {}
    	tab = line.split(" ")
    	if (tab[0] == "test"):
    		print "your the boss"
        print tab

    def do_exit(self, line):
    	return True

    def do_EOF(self, line):
        return True

    def emptyline(self):
        pass

    def do_yaml(self, line):
        for d in doc:
            print d+" : "
            for c in doc[d]:
                print c+" : "+doc[d][c]
            print "\n"

if __name__ == '__main__':
    init()
    Prompt().cmdloop()