#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when we have (a ~> b ~< a); which takes precedence?

a = Job('print.py', 'care');
b = Job('print.py', 'ful');

run(a ~> b ~< a);
