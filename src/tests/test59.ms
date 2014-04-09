#!/usr/bin/maestro

master("0.0.0.0:6379")

# check lists of scripts - what happens when the user passes a list with malicious objects

list = [' ', ' ']
list.each(var){
	a = Job('print.py', var)
	run(a)
}
