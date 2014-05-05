#!/usr/bin/python

#Usage "python test_framework.py <1,2...>"  or "python test_Framework.py all"

import sys
from subprocess import Popen, PIPE, STDOUT
from colorama import init,Fore, Back, Style
init()

global failCount
failCount = 1

def parseErr(stderr):
	global failCount

	if not stderr:
		print (Fore.GREEN + "Maestro Program Passed")
	else:
		print (Fore.RED + "Maestro Program Failed")
		failCount = failCount + 1
	print "**************************"
def parseOut(stdout):
	global failCount

	if "Illegal" in stdout:
		print (Fore.RED + "Test Failed - Illegal token resulting in syntax error")
		failCount = failCount + 1
	else:
		print (Fore.GREEN + "Test Passed!")

if len(sys.argv)!= 2:
	print "Wrong input. Usage: 'python test_bash.py <1,2,...>' or 'python test_bash.py all'"

elif sys.argv[1] == 'all':
	for i in range(1,78):
		oldCount = failCount
		cmd = 'python myacc.py tests/test'+str(i)+'.ms'
		p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
		stdout, stderr = p.communicate()
		print (Fore.BLUE + "-------------------------------")
		print "TEST"+str(i)
		print "-------------------------------"
		if stderr:
			print (Fore.BLACK + stderr)
		parseErr(stderr)
		if stdout:
			print (Fore.BLACK + stdout)
		else:
			print "Empty Output"
		parseOut(stdout)

		if failCount-oldCount == 2:
			failCount = failCount - 1

	failCount = failCount - 1
	passCount = 77 - failCount
	print (Fore.BLUE + "**************************")
	print (Fore.BLUE + "Tests Passed : " + str(passCount)+"/77")
	print "**************************"
else:
	cmd = 'python myacc.py tests/test'+sys.argv[1]+'.ms'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
	stdout, stderr = p.communicate()
	print (Fore.BLUE + "-------------------------------")
	print "TEST"+sys.argv[1]
	print "-------------------------------"
	if stderr:
		print (Fore.BLACK + stderr)
	parseErr(stderr)
	if stdout:
		print (Fore.BLACK + stdout)
	else:
		print "Empty Output"
	parseOut(stdout)