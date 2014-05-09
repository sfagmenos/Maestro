#!maestro
#master("0.0.0.0:6379")
# check what happens when file is indivisible
a = Job('split.rb', 'one_character_file.data')
maps = maps(a, 'map.rb')
green = reduce(maps, 'reduce.rb')
run(geen)
