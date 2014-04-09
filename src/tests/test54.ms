#!/usr/bin/maestro

master("0.0.0.0:6379")

#check if parentheses affect precedence correctly. ex (3+4)*2 returns 14 and not 11

a = (3+4)*2
print a