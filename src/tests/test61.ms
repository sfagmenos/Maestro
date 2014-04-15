#!maestro
#master("0.0.0.0:6379")
# check lists of scripts - what happens when user gives more than required number of input arguments?

a = Job('print.py', ‘foo’, ‘bar’)
run(a)