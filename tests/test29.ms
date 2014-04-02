#!/usr/bin/maestro

master("0.0.0.0:6379");

# check use of the operator /, when we divide by zero;

c = 0;
d = 8; 

# this should error
range(d/c).each(var){
	a = Job('print.py', var);
	run(a);
}

# this should not error
b = Job('print.py', (d/c));



