#!/usr/bin/maestro

master("0.0.0.0:6379");

# check what happens when program is nonexistent

a = Job('nonexistent_program.py', 'trythis');
run(a);
