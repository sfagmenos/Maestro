#!maestro
#master("0.0.0.0:6379")
#check use of the operator == comparison operations

a = Job('print.py', ‘foo’)
if (1==1)
{
	run(a)
}