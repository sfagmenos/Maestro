#!/usr/bin/maestro

master("0.0.0.0:6379");

check use of consistent types for: FLOAT and FLOAT

c = 2.0; #float
d = 4.2; #float

print c+d;
}
 