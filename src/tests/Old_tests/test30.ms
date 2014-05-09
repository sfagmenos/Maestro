#!maestro
#master("0.0.0.0:6379")
# check use of the operator *
c = 5
d = 8
range(d).each(var){
	range(c).each(varr){
		a = Job('print.py', var*varr)
		run(a)
	}

}