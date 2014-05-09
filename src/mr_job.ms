#! maestro

a = Job("./cut.rb", "./all.txt", "3");

maps = map(a, "./count.rb", 3);
red = reduce(maps, "./reduce.rb");
run(a, maps, red);
