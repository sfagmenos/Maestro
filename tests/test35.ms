#!maestro
#master("0.0.0.0:6379")
# check what happens to map function when file is corrupted
a = Job('split.rb', 'corrupted_file.data')
maps = map(a, 'map.rb')
green = reduce(maps, 'reduce.rb')
run(green)