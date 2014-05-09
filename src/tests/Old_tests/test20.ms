#!maestro
#master("0.0.0.0:6379")
# check that list is being run in order
list = ['input1.txt', 'input2.txt', 'input3.txt']
jobList = []
list.each(listitem){
	a = Job('print.py', listitem)
	jobList = jobList + a
}
run(jobList)
