#!/usr/bin/maestro

master("0.0.0.0:6379");

check use of consistent types for: FLOAT and INT

c = 2.0; #float
d = 4; #int

print c+d;
}
 