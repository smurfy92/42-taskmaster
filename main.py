import cmd
from yaml import load, dump
from proccess import *

processes = {}

promptinit = """\n
|
|  ::::::::::::::     :::::::: :::    :::  :::   :::      :::     ::::::::::::::::::::::::::::::::::::::
|     :+:  :+: :+:  :+:    :+::+:   :+:  :+:+: :+:+:   :+: :+:  :+:    :+:   :+:    :+:       :+:    :+:
|    +:+ +:+   +:+ +:+       +:+  +:+  +:+ +:+:+ +:+ +:+   +:+ +:+          +:+    +:+       +:+    +:+
|   +#++#++:++#++:+#++:++#+++#++:++   +#+  +:+  +#++#++:++#++:+#++:++#++   +#+    +#++:++#  +#++:++#:
|  +#++#+     +#+       +#++#+  +#+  +#+       +#++#+     +#+       +#+   +#+    +#+       +#+    +#+
| #+##+#     #+##+#    #+##+#   #+# #+#       #+##+#     #+##+#    #+#   #+#    #+#       #+#    #+#
|######     ### ######## ###    ######       ######     ### ########    ###    #############    ###
|____________________________________________________________________________________________
"""

def init():
    rows, columns = os.popen('stty size', 'r').read().split()
    print "\033[92m"+promptinit+"\033[0m"
    with open('test.conf', 'r') as f:
        doc = load(f)
    for proc in doc:
        processes[proc] = Proccess(proc, doc[proc])

class Prompt(cmd.Cmd):
    prompt = "\033[92mTaskmaster -> \033[0m"
    def do_start(self, line):
        t = line.split(" ")
        if (t[0] in processes):
            processes[t[0]].start()
        else:
            if t[0]:
                print "No program "+ t[0]
            else:
                print "You need to specify program"

    def do_stop(self, line):
    	tab = line.split(" ")
        if (tab[0] in processes):
            if processes[tab[0]].statuss == "RUNNING":
                processes[tab[0]].stop()
            else:
                print "Program not running"
        else:
            if tab[0] == "all":
                for p in processes:
                    if processes[p].statuss == "RUNNING":
                        processes[p].stop()
            elif tab[0]:
                print "No program "+ tab[0]
            else:
                print "You need to specify program"

    def do_restart(self, line):
        tab = line.split(" ")
        if (tab[0] in processes):
            if processes[tab[0]].statuss == "RUNNING":
                processes[tab[0]].stop()
                processes[tab[0]].start()
            else:
                print "Program not running"
        else:
            if tab[0]:
                print "No program "+ tab[0]
            else:
                print "You need to specify program"

    def do_status(self, line):
        tab = line.split(" ");
        if tab[0] == "":
            for p in processes:
                if processes[p]:
                    processes[p].status()
        else:
            if tab[0] in processes:
                processes[tab[0]].status()
            else:
                print "no process named "+tab[0]

    def do_reload(self, line):
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