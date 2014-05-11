#!maestro
#master("0.0.0.0:6379")
# check to make sure lists don't have to be declared outside of loops
list = ['input1.txt', 'input2.txt', 'input3.txt']
list.each(var){
	a = Job('print.py', var)
	b = Job('print.py', var+'change')
	l1 = l1 + a
	l2 = l2 + b
}
run(l1 -> l2)
