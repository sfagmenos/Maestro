#!/usr/bin/maestro

master("0.0.0.0:6379")

#check use of the operator OR logical operations

a = Job('print.py', ‘foo’)
if (3>4 OR 2>1)
{
	run(a)
}