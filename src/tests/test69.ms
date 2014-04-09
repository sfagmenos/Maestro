#!/usr/bin/maestro

master("0.0.0.0:6379")

#check use of consistent types for: FLOAT and STRING

c = 2.0; #float
d = 'bar'; #string

if(c == d){
	a = Job('print.py', 'foo')
	run(a)
}