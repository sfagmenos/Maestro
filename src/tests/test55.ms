#!/usr/bin/maestro

master("0.0.0.0:6379")

#check behaviour of program if multiple dependencies are defined between jobs

a = Job('print.py', ‘foo’)
b = Job('print.py', ‘bar’)

run(a -> ~> b)