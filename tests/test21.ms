#!/usr/bin/maestro

master("0.0.0.0:6379");

# check whether (((a -> b) -> b) -> b) -> b) is different from (a -> b -> b -> b)

a = Job('print.py', 'one');
b = Job('print.py', 'two');

# maybe we need to add an evaluate expression function?

run((((a -> b) -> b) -> b) -> b));
run((a -> b -> b -> b));
