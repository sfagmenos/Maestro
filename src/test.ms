#!maestro

int i = 9;
a = Job("ls", ".");
b = Job("ls", "/");
a->b;
run(a,b);
