#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when list is empty?

list = [];
list.each(var){
	a = Job(var, 'trythis');
	run(a);
}

