#!maestro
#master("0.0.0.0:6379")
#check use of consistent types for: BOOL and FLOAT

c = true; #bool
d = 12.4; #float

if(c < = d){
	a = Job('print.py', 'foo')
	run(a)
}