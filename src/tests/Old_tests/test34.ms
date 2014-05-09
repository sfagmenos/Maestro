#!maestro
#master("0.0.0.0:6379")
# check what happens when jobs are redeclared inside loops
l1 = []
l2 = []
list = ['input1.txt', 'input2.txt', 'input3.txt']
list.each(var){
	a = Job('print.py', var)
	l1 = l1 + a
	l2 = l2 + a
}
run(l1 => l2)