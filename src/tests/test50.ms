#!maestro
#master("0.0.0.0:6379")
#check use of the operator >= comparison operations

a = Job('print.py', ‘foo’)
if (4>=3)
{
	run(a)
}