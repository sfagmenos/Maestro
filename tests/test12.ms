#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when job doesn't have enough input arguments

a = Job('program_takes_two_inputs.py', 'trythis');
run(a);

