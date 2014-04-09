#!maestro
#master("0.0.0.0:6379")
# check the scope of variables within loops - does it retain previous value?
range(10).each(i){
	k = i+1
	a = Job('print.py', k)
	b = Job('print.py', 'trythis')
	c = a~b
}
run(b -> c)