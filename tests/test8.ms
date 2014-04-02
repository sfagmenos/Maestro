#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when jobs depend on themselves

a = Job('print.py', 'cool');

run(a -> a -> a);