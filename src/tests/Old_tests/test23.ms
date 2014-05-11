#!maestro
#master("0.0.0.0:6379")
# check precedences of the different operators, ie a -> b <-> c should be the same as a -> (b <-> c)
a = Job('print.py', 'one')
b = Job('print.py', 'two')
# maybe we need to add an evaluate expression function?
run(a -> b <-> c)
run(a -> (b <-> c))
