#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when booleans are fed to each statement

L = [true, false, false, true];

L.each(var){
	
	a = Job('evaluate.py', true);
	print(a);
}
