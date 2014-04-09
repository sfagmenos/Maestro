#!/usr/bin/maestro

master("0.0.0.0:6379");

check use of consistent types for: INT and INT

c = 2; #int
d = 3; #int

range(d*c).each(var){
	a = Job('print.py', var);
	run(a);
}
 