import subprocess
import sys
import os
import time
import shutil

import Tkinter
import tkMessageBox

import check_network

def test_url(url, number, interval, percentage, use_cgn=False, use_proxy=False):
	#print "::: checking network :::"
	while not check_network.working_fine(url, number):
		print "::: there seems to be an issue :::"
		tkMessageBox.showwarning("CGN - Network Connectivity Issue",
			"Sorry, your computer does not seem connected to the internet. Please press 'OK' after ensuring it is connected. Thank you.")
		if check_network.working_fine(url, number):
			check_network.restart_local_proxy()

	if number % 2 == 0:
		use_compression = True
	else:
		use_compression = False

	#print "::: testing url:", url

	number = str(number)
	backup_num = str(number)

	if use_proxy: number += '_cgn'
	else: number += '_nocgn'

	if not os.path.exists(str(number)):
		os.makedirs(str(number))

	#print "Initializing measurement sequence."

	REDIRECT = ">>/dev/null 2>&1"
	#REDIRECT = ""
	
	cmd = "python bmp_test.py -u {0} -p {1} -H 1 -t {2} {3}".format(url, number, interval, REDIRECT)
	if use_proxy: 
		#print "::: Testing with CGN :::"
		if use_compression:
			cmd = "python bmp_test.py -u {0} -p {1} -H 1 -t {2} -c 1 -x 1 {3}".format(url, number, interval, REDIRECT)
		else:
			cmd = "python bmp_test.py -u {0} -p {1} -H 1 -t {2} -c 1 {3}".format(url, number, interval, REDIRECT)
	else:
		#print "::: Testing without CGN :::"
		pass

	os.system(cmd)
	os.system("sudo ./kill_chrome.sh >>/dev/null 2>&1")
	cmd = "echo \"\" | netcat 127.0.0.1 8081"
	os.system(cmd)

	#print "Initializing visual completion analysis."
	cmd = "python viz_complete_time.py -p {0} -t {1} -x {2} -l 1 {3}".format(number, interval, percentage, REDIRECT)
	subprocess.call(cmd, shell=True)

	#print "Intializing image clean up sequence."
	cmd = "python clean_up_images.py -p {0} {1}".format(number, REDIRECT)
	subprocess.call(cmd, shell=True)
			
	tmp = 0
	if use_proxy: tmp = 1

	#print "Reporting to server"
	if not use_proxy: backup_num = str(-1)
	cmd = "python report_url.py {0} --cgn_used={1} {2} {3} {4}".format(number, tmp, url, backup_num, REDIRECT)
	subprocess.call(cmd, shell=True)

PERCENTAGE = 90
INTERVAL = 0.2

if __name__ == '__main__':
	with open(sys.argv[1]) as f:
		start_time = time.time()
		time_limit = -1
		handle_proxy = False
		if len(sys.argv) > 2: time_limit = int(sys.argv[2]) * 60
		if len(sys.argv) > 3:
			if "--handleproxy" in sys.argv[3]:
				handle_proxy = True


		i = 1
		for line in f:
			cgn = False
			if handle_proxy:
				cgn = True
				print "Testing URL:", line.strip()
				#subprocess.call("sudo ./proxy_off.sh >>/dev/null 2>&1", shell=True)				
				test_url(line.strip(), i, INTERVAL, PERCENTAGE, cgn, False)

				#if i % 5 == 0:
				#	subprocess.call("sudo ./proxy_on.sh 127.0.0.1 9090 >>/dev/null 2>&1", shell=True)
				#else:	
				#	subprocess.call("sudo ./proxy_on.sh 127.0.0.1 8080 >>/dev/null 2>&1", shell=True)								
				test_url(line.strip(), i, INTERVAL, PERCENTAGE, cgn, True)
				# calculate_correctness(i)
				print "URL", line.strip(), "testing done. Moving forward to next URL."												

			else: test_url(line.strip(), i, INTERVAL, PERCENTAGE, cgn)
			i += 1

			elapsed_time = time.time() - start_time
			if (elapsed_time > float(time_limit)):
				break

		print "Experiment ended. Thank you for your time."