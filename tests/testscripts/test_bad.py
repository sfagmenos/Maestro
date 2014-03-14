import time
import fcntl

# variable is undefined fail
team = ['ren\n', 'arun\n', 'georgios\n', 'mathias', 'vaggelis\n', 'junde\n', 'aho\n', 'imaginary\n']

# file does not exist fail

# file is corrupted fail

i = 0
f = open('team.txt', 'a+')
g = open('teamio.txt', 'rw')
lines = g.readlines()
fcntl.flock(f, fcntl.LOCK_EX)
fcntl.flock(g, fcntl.LOCK_EX)
for teammate in team + lines:
	if i%2 == 0:
		time.sleep(1)
		f.write(teammate+'\n')
	else:
		f.write(teammate+teammate+'\n')
	i = i+1
fcntl.flock(f, fcntl.LOCK_UN)
fcntl.flock(g, fcntl.LOCK_EX)

f.close()
