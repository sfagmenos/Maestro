#!maestro
#master("0.0.0.0:6379")
# check map against a for loop
a = Job('split.rb', 'file1.data')
maps = map(a, 'map.rb')
green = reduce(maps, 'reduce.rb')
run(geen)
b = Job('split2.rb', 'file1.data')
b.each(job){
	
	run(b)
}
