#!/usr/bin/maestro

master("0.0.0.0:6379");

# check lists of scripts - what happens when the user passes a list that has both valid and malicious objects

list = ['test.py', ' '];
list.each(var){
	a = Job('print.py', var);
	run(a)
}
