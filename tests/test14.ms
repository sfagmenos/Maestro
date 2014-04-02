#!/usr/bin/maestro

master("0.0.0.0:6379");

# test list concatenation

l1 = ['script1.py', 'script2.py'];
l2 = ['script3.py', 'script4.py'];

# test these two against each other
l = l1 + l2;
l.each(item){
	a = Job(item, 'trythis');
	run(a);
}

# they should give the same results
run(l);
