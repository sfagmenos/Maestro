#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when you give the reduce function something other than the output of a map function.

a = Job('split.rb', 'file1.data');
b = Job('split.rb', 'file2.data');
c = Job('split.rb', 'file3.data');
maps = [a, b, c];
green = reduce(maps, 'reduce.rb');

run(green);
