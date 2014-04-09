#!/usr/bin/maestro

master("0.0.0.0:6379")

#check use of the operator /= assignment operations

a = Job('print.py', ‘foo’)
for(i=8;i/=2;i>=1)
{
	run(a)
}