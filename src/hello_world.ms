#! maestro

service("systems-yellow.cs.columbia.edu:6379");

a = Job("./hello_world.sh", "I waited for 1 second");
b = Wait(1);

c = Job("./hello_world.sh", "I waited for 5 seconds");
d = Wait(3);


b->a;
d->c;
run(a,b,c,d);
