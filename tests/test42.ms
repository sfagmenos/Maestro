#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when a job is run without being declared

a = Job('print.py', ‘foo’);
c = Job('print.py' ‘bar’);

run(a -> b -> c);  # Job b is not declared