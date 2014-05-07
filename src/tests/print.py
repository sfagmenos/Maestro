#!/usr/local/bin/python

import sys

print sys.argv[1]

f = open('TestsOutput/check.txt','w+')
f.write(sys.argv[1])
f.close()