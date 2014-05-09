#! maestro

# a = Job("ls", ".");

maps = map(["./1.txt", "./2.txt", "./3.txt"], "count.rb", 3);
red = reduce(maps, "reduce.rb");
run(maps, red);
