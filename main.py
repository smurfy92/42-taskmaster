import cmd
from yaml import load, dump
from proccess import *
import sys
import threading

processes = {}

promptinit = """\n
 __________________________________________________________________________________________________________
|                                                                                                          |
|   ::::::::::::::     :::::::: :::    :::  :::   :::      :::     ::::::::::::::::::::::::::::::::::::::  |
|      :+:  :+: :+:  :+:    :+::+:   :+:  :+:+: :+:+:   :+: :+:  :+:    :+:   :+:    :+:       :+:    :+:  |
|     +:+ +:+   +:+ +:+       +:+  +:+  +:+ +:+:+ +:+ +:+   +:+ +:+          +:+    +:+       +:+    +:+   |
|    +#++#++:++#++:+#++:++#+++#++:++   +#+  +:+  +#++#++:++#++:+#++:++#++   +#+    +#++:++#  +#++:++#:     |
|   +#++#+     +#+       +#++#+  +#+  +#+       +#++#+     +#+       +#+   +#+    +#+       +#+    +#+     |
|  #+##+#     #+##+#    #+##+#   #+# #+#       #+##+#     #+##+#    #+#   #+#    #+#       #+#    #+#      |
| ######     ### ######## ###    ######       ######     ### ########    ###    #############    ###       |
|                                                                                                          |
|__________________________________________________________________________________________________________|
"""

def error_config(name):
    log.error("Error in config file " + name)
    print "Error in config file in "+ name
    sys.exit(0)
def check_data(data):
    for d in data:
        if "command" not in data[d] or type(data[d]["command"]) is not str:
            error_config("command")

def loop():
    while True:
        copy = processes.copy()
        for proc in copy:
            if copy[proc].proccess:
                copy[proc].check()

def init():
    try:
        with open('test.conf', 'r') as f:
            doc = load(f)
    except:
        print "Error in config file"
        log.error("Error in config file")
        sys.exit(0)
    check_data(doc)
    for proc in doc:
        processes[proc] = Proccess(proc, doc[proc])
    print "\033[92m"+promptinit+"\033[0m"


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
            if processes[tab[0]].statuss == "RUNNING" or processes[tab[0]].statuss == "STARTING":
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
    	try:
            with open('test.conf', 'r') as f:
                newdoc = load(f)
        except:
            print "Error in config file"
            log.error("Error in config file")
            sys.exit(0)
        todel = []
        check_data(newdoc)
        for d in processes:
            if d not in newdoc:
                if processes[d].statuss == "STARTING" or processes[d].statuss == "RUNNING":
                    processes[d].proccess.terminate()
                todel.append(d)
            else:
                if newdoc[d]["command"] != processes[d].command and processes[d].statuss == "STARTING" or processes[d].statuss == "RUNNING":
                    processes[d].stop()
                processes[d] = Proccess(d, newdoc[d])
        for k in todel:
            processes.pop(k, None)
        for p in newdoc:
            if p not in processes:
                processes[p] = Proccess(p, newdoc[p])

    def do_exit(self, line):
        for p in processes:
            if processes[p].statuss == "RUNNING" or processes[p].statuss == "STARTING":
                processes[p].stop()
    	return True

    def do_EOF(self, line):
        print ""
        for p in processes:
            if processes[p].statuss == "RUNNING" or processes[p].statuss == "STARTING":
                processes[p].stop()
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
    th = threading.Thread(target=loop)
    th.daemon = True
    th.start()
    Prompt().cmdloop()