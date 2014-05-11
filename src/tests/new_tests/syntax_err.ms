#!maestro
// this is also a comment

a = Job("./tmp/test.sh", "bla");
b= Job("./tmp/test.sh", "foo")
c = Job("./tmp/test.sh", "bla");
run(a);