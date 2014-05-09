#!maestro
// this is also a comment

a = Job("./tmp/test.sh", "bla");
b= Job("./tmp/test.sh", "foo");
c = Job("./tmp/test.sh", "bla");
d= Job("./tmp/test.sh", "foo");
e = Job("./tmp/test.sh", "bla");
f= Job("./tmp/test.sh", "foo");
g = Job("./tmp/test.sh", "bla");
h= Job("./tmp/test.sh", "foo");
i = Job("./tmp/test.sh", "bla");
j= Job("./tmp/test.sh", "foo");
k = Job("./tmp/test.sh", "bla");
l= Job("./tmp/test.sh", "foo");



run(a->b->c->d->e->f->g->h->i->j->k->l);

