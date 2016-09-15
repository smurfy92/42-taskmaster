import subprocess
import cmd

class Prompt(cmd.Cmd):
    """Simple command processor example."""
    prompt = "\033[92mTaskmaster -> \033[0m"
    subprocess.Popen(['echo', 'coucou'])
    def do_start(self, line):
    	tab = {}
    	tab = line.split(" ")
    	if (tab[0] == "test"):
    		print "your the boss"
        print tab

    def do_stop(self, line):
    	tab = {}
    	tab = line.split(" ")
    	if (tab[0] == "test"):
    		print "your the boss"
        print tab

    def do_reload(self, line):
    	tab = {}
    	tab = line.split(" ")
    	if (tab[0] == "test"):
    		print "your the boss"
        print tab

    def do_shutdown(self, line):
    	tab = {}
    	tab = line.split(" ")
    	if (tab[0] == "test"):
    		print "your the boss"
        print tab

    def do_exit(self, line):
    	return True

    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    Prompt().cmdloop()