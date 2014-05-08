#! maestro

a = Job("ls", ".");
b = Job("ls", "/");

maps = map(a, "map.rb", 10);
red = reduce(maps, "reduce.rb");
run(maps, red);
