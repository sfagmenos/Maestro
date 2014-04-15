#!maestro
#master("0.0.0.0:6379")
# Check hard circular dependencies embedded within a dependency parameter

a = Job('print.py', ‘foo’)
b = Job('print.py', ‘bar’)
c = Job('print.py' ‘blah’)

run(a -> b -> a -> c)