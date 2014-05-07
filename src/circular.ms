#!maestro
a = Job("./tmp/test.sh");
b = Job("./tmp/test.sh");
c = Job("./tmp/test.sh");
d = Job("./tmp/test.sh");
a->b->c;
run(a,b,c)
