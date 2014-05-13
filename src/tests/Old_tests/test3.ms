#!maestro
#master("0.0.0.0:6379")
# check soft malicious dependencies
a = Job('malicious.py', 'cheer')
b = Job('print.py', 'us')
run(a ~> b)
