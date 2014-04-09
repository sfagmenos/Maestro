#!/usr/bin/maestro

master("0.0.0.0:6379")

#check use of consistent types for: BOOL and INT

c = true; #bool
d = 23; #int

if(c > d){
	a = Job('print.py', 'foo')
	run(a)
}