#!/usr/bin/maestro

master("0.0.0.0:6379");

#check use of the operator AND comparison operations

a = Job('print.py', ‘foo’);
if (4==4 AND 1==1)
{
	run(a);
}