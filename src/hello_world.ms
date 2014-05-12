#! maestro

#service("systems-yellow.cs.columbia.edu:6379");

a = Job("./hello_world.sh", "Hello");
b = Job("./hello_world.sh", "World");
c = Job("./hello_world.sh", "!");
d = Wait(3);


a->b->d->c;
run(a,b,c,d);
