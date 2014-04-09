#!/usr/bin/maestro

master("0.0.0.0:6379");

#check scenario where parameter of wait is given of incompatible type

a = Job('print.rb', 'foo');
b = Job('print.rb', 'bar');
c = Job('print.rb', 'blah');

run(a -> b -> Wait(4.5) -> c); #Parameter of wait not INT