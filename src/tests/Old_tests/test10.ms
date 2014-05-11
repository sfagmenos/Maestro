#!maestro
#master("0.0.0.0:6379")
# check what happens when we just run wait expressions in parallel?
a = Job('print.py', 'cool')
b = Job('print.py', 'it')
c = Job('print.py', 'now')
run(wait(10) ~ wait(20))