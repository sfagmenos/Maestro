a = Job("./print.rb", "hello");
b = Job("./print.rb", "world");
c = Job("./print.rb", "!");

d = a ~> b ~> c;
run(d);

a1 = Job("./print.rb", "hello");
b2 = Job("./print.rb", "world");
c3 = Job("./print.rb", "!");

d = (a1 <~> b2) ~> c3;
run(d);
