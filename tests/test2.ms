#!/usr/bin/maestro

master("0.0.0.0:6379");

# check soft circular dependencies with strings

a = Job('print.py', 'cheer');
b = Job('print.py', 'us');
c = Job('print.py' 'on');

run(a ~> b ~> c ~> a);