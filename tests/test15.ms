#!/usr/bin/maestro

master("0.0.0.0:6379");

# run dependencies on different lines that contradict each other

l1 = ['script1.py', 'script2.py'];
l2 = ['script3.py', 'script4.py'];

a = Job('print.py', 'care');
b = Job('print.py', 'ful');

run(a->b);
run(b->a);
