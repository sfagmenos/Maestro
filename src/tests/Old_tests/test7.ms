#!maestro
#master("0.0.0.0:6379")
# check what happens when hard equivalences and soft equivalences are combined.
a = Job('print.py', 'cool')
b = Job('print.py', 'it')
c = Job('print.py', 'now')
run(a <-> b ~ c)