#!maestro

a = Job("ls", ".");
b = Job("ls", "/");
c = Job("ls", "/");

a->b->c;
run(a,b,c);
