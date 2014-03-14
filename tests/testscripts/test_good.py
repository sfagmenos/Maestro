#!/usr/local/bin/python

import time
import fcntl

team = ['REN', 'ARUN', 'GEORGIOS', 'MATHIAS', 'VAGGELIS', 'JUNDE', 'AHO', 'IMAGINARY']

i = 0
f = open('team.txt', 'a+')
fcntl.flock(f, fcntl.LOCK_EX)
for teammate in team:
	if i%2 == 0:
		time.sleep(3)
		f.write(teammate+'\n')
	else:
		time.sleep(8)
		f.write(teammate+teammate+'\n')
	i = i+1
fcntl.flock(f, fcntl.LOCK_UN)

f.close()
