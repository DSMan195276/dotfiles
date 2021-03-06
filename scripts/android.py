#!/usr/bin/python2 -tt

import subprocess

# input keyevent 26 !! 26 turns off the screen!
# input keyevent 66 --> ENTER

# adb subprocess
adb = None

class _Getch:
    """Gets a single character from standard input.  Does not echo to the screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def main():
	# Listen for user input including ENTER
	print 'Input your text'
	global adb
	# Needs the stdout PIPE otherwise gets automatically redirected in my stdout
	adb = subprocess.Popen(["adb", "shell"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	try:
		while(True):
			process_input()

	except KeyboardInterrupt: #Ctrl-C
		print "\nCtrl^C received --> dying now"
		adb.stdin.write("exit\n")
		adb.terminate()

def process_input():
	user_input = getch()
	# raw_input('')
	# If input is empty or only is ENTER
	# if not user_input or user_input == "\n":
	#	return
	# Split sentence into words
	# words = user_input.split(' ');

	# loop on all words
	#for word in words:
		# Call adb shell input
        #		send_word(word)
#		send_space()

#	send_eol_combo()
	send_word(user_input)

def send_eol_combo():
	send_key(22) # Right to reach the Send button
	send_enter() # ENTER to push the Send button
	send_key(21) # Left to give the focus back to the text input
	return

def send_space():
	send_key(62)

def send_enter():
	send_key(66)

# Key should be an int
def send_key(key):
	adb.stdin.write("input keyevent %d\n" % key)

def send_word(text):
	# Escape characters that adb doesn't like 
	escape_chars = {
			"'": "\\'",
			'"': '\\"',
			"(": "\\(",
			")": "\\)"
	}
	for key, value in escape_chars.iteritems():
		text = text.replace(key, value)
	# Send the escaped text to adb
	adb.stdin.write("input text %s\n" % text)

if __name__ == '__main__':
	main()


