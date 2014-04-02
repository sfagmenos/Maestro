#!/usr/bin/maestro

master("0.0.0.0:6379");

# check use of the operator + in different contexts, ie list concatenation, arithmetic operation, string concatenation

l1 = [e+'.py', f+'.py'];

e = 'too';
f = 'much';

a = Job('print.py', e+f);
b = Job('print.py', f+e);

c = Job('print.py', 5+4);
d = Job('print.py', 8%2);

run((a<->b)~>(c->d));

