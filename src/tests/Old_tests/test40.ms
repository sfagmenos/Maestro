#!maestro
#master("0.0.0.0:6379")
# check what happens when we give list to map function.
a = Job('split.rb', 'file1.data')
b = Job('print.py', 'try')
c = Job('print.py', 'this')
maps = map([a,b,c], 'map.rb')
green = reduce(maps, 'reduce.rb')
run(green)
