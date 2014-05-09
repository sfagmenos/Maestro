#!maestro
#master("0.0.0.0:6379")
# check what happens when a -> b but a takes as input a file that b produces, ie when explicit dependencies contradict implicit dependencies?
a = Job('print.py', 'file_b_creates.txt')
b = Job('print2.py')
run(a -> b)