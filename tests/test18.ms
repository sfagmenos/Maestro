#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when we string together arithmetic operations

list = [];
list.each(var){
	a = Job(var, 'trythis');
	b = Job('print.py', 'trythis')
	c = a~b;
	list = list + c;
}