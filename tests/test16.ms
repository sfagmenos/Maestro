#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when dependency is on empty list

l1 = [];
l2 = ['script1.py', 'script2.py'];
l3 = ['script3.py', 'script4.py'];

run((l1 <-> l2) -> l3);

# these should be equivalent
run(l2 -> l3)
