#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when jobs are redeclared inside loops

a = Job('print2.py', 2);

list = ['input1.txt', 'input2.txt', 'input3.txt'];
list.each(var){
	a = Job('print.py', var);
	b = Job('print.py', var+'change');
	run(a -> b);
}
