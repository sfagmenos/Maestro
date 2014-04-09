#!/usr/bin/maestro

master("0.0.0.0:6379");

check use of consistent types for: BOOL and STRING

c = true; #bool
d = "test"; #string

if(c == d){
	a = Job('print.py', 'foo');
	run(a);
}