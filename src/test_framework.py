#!/usr/bin/python

#Usage "python test_framework.py <1,2...>"  or "python test_Framework.py all"

import sys
from subprocess import Popen, PIPE, STDOUT
from colorama import init,Fore, Back, Style
init()
global output
output= ""
global failCount
failCount = 1
files=['my_file','comment','undeclared_job','undeclared_job2','hard_dependency','multiple_declaration','multiple_declaration2','multiple_run', 'syntax_err', 'circular_dependency', 'self_dependency']
#def parseErr(stderr):
#	global failCount

#	if not stderr:
#		print (Fore.GREEN + "Maestro Program Passed")
#	else:
#		print (Fore.RED + "Maestro Program Failed")
#		failCount = failCount + 1
#	print "**************************"
def parseOut(stdout, filename):
	global failCount
	global output
	with open ("TestsOutput/check.txt", "r") as myfile:
		data=myfile.read().replace('\n', '')
		
		
	if "Illegal" in stdout:
		print (Fore.RED + "Test Failed - Illegal token resulting in syntax error")
		failCount = failCount + 1
		with open ("tests/new_tests/log.txt", "a") as myfile:
			myfile.write(filename+ "      -Failed"+"\n")
			myfile.write("********** \n")
			myfile.write(stdout+"\n")

	elif "Syntax error" in stdout:
		failCount = failCount + 1
		print (Fore.RED + "Test Failed - Syntax error in input")
		with open ("tests/new_tests/log.txt", "a") as myfile:
			myfile.write(filename+ "      -Failed"+"\n")
			myfile.write("********** \n")
			myfile.write(stdout+"\n")

	elif (data!="check"):
		
		print (Fore.RED + "Test Failed - Expected output not found at file")
		print "**************************"
		print (Fore.BLACK+ "Expected Output: check"+" \nOutput read at file: "+ data)
		print "\n"
		with open ("tests/new_tests/log.txt", "a") as myfile:
			myfile.write(filename+ ".ms   -Failed"+"\n")
			myfile.write(stdout+"\n")

	
	else:
		print (Fore.GREEN + "Test Passed!")
		with open ("tests/new_tests/log.txt", "a") as myfile:
			myfile.write(filename+ ".ms   -Passed"+"\n")
			myfile.write("********** \n")
			myfile.write(stdout+"\n")

	

if len(sys.argv)!= 2:
	print "Wrong input. Usage: 'python test_bash.py <1,2,...>' or 'python test_bash.py all'"

elif sys.argv[1] == 'all':
	with open ("tests/new_tests/log.txt", "w") as myfile:
			myfile.write("")
	for i in range(0,8):

		output = str(i)

		oldCount = failCount
		cmd = './maestro tests/new_tests/'+files[i]+'.ms'
		p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
		stdout, stderr = p.communicate()
		print (Fore.BLUE + "-------------------------------")
		print "TEST "+files[i]
		print "-------------------------------"
		#if stderr:
			#print (Fore.BLACK + stderr)
		#parseErr(stderr)
		if stdout:
			print (Fore.BLACK + stdout)
			parseOut(stdout, files[i])
		else:
			print (Fore.BLACK + "Empty Output")
			print ""
		

		#if failCount-oldCount == 2:
			failCount = failCount - 1

	#failCount = failCount - 1
	#passCount = 77 - failCount
	#print (Fore.BLUE + "**************************")
	#print (Fore.BLUE + "Tests Passed : " + str(passCount)+"/77")
	#print "**************************"
else:
	with open ("tests/new_tests/log.txt", "w") as myfile:
			myfile.write("")
	output = sys.argv[1]
	cmd = './maestro tests/new_tests/'+sys.argv[1]+'.ms'
	p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
	stdout, stderr = p.communicate()
	#print "stdout is "+stdout
	print (Fore.BLUE + "-------------------------------")
	print "TEST "+sys.argv[1]
	print "-------------------------------"
	print (Fore.BLACK + "")
	#if stderr:
		#print (Fore.BLACK + stderr)
	#parseErr(stderr)
	if stdout:
		print (Fore.BLACK + stdout)
		parseOut(stdout, sys.argv[1])

	else:
		print (Fore.BLACK + "Empty Output")
		print ""
	