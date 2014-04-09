#!/usr/bin/maestro

master("0.0.0.0:6379")

#check behaviour of run() if jobs are declared within run() parameters

a = Job('print.py', ‘foo’)
b = Job('print.py', ‘bar’)

run((a = Job('print.py', ‘foo’)) -> (b = Job('print.py', ‘bar’))