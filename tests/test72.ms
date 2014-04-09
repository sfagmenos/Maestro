#!/usr/bin/maestro

master("0.0.0.0:6379");

check use of consistent types for: BOOL and BOOL

c = true; #bool
d = false; #float

if(c == d){
	a = Job('print.py', 'foo');
	run(a);
	print "success";
}