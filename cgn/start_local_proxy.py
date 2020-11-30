from Tkinter import *
import tkMessageBox
import subprocess
import os
import sys

master = Tk()



ask = Label(master, text="Do you consent to the following?")
ask.pack()


w = Label(master, text="(If you consent and click the 'Yes' button, \nplease wait for a message box before beginning the experiment. This may take several minutes)")
w.pack()

listbox = Listbox(master, bd=0)
listbox.pack(fill="both",expand=True)
master.minsize(height=500, width=600)

scrollbar = Scrollbar(listbox)
scrollbar.pack(side=RIGHT, fill=Y)

with open("consent.txt") as f:
	for line in f:
		listbox.insert(END, line[:-1])

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def show_url_list():
	frame = Toplevel(master, bd=2, relief=SUNKEN)
	frame.minsize(400,400)

	ask = Label(frame, text="Can we load the following urls on your device?")

	ask.pack()
	

	conf = Button(frame, text="Confirm", command=start_proxy)
	conf.pack()
	deny = Button(frame, text="Reject", command=frame.quit)

	deny.pack()

	scrollbar = Scrollbar(frame)
	scrollbar.pack(side=RIGHT, fill=Y)
	
	listbox = Listbox(frame, bd=0)
	listbox.pack(side=BOTTOM, fill="both",expand=True)

	subprocess.call("sudo python shuffle_dataset.py curated_list.csv url_list.txt", shell=True)

	with open("url_list.txt") as f:
		for line in f:
			listbox.insert(END, line[:-1])
	
	listbox.config(yscrollcommand=scrollbar.set)
	scrollbar.config(command=listbox.yview)

def start_proxy():
	tkMessageBox.showinfo("Please wait!", "After pressing OK, please wait for a message box confirming startup completion to appear before beginning the experiment. This may take several minutes")
	w.config(text="Please do not close this window during the experiment")
	b.config(state="disabled")
	print "Loading..."
	os.chdir("./lp/")
	os.system("sudo killall java >>/dev/null 2>&1")
	os.system("sudo fuser -k 8080/tcp >> /dev/null 2>&1")
	os.system("rm -rf proxy_log.log")
	os.system("echo start >> proxy_log.log")
	subprocess.call("sudo /home/mooc/jre1.8.0_144/bin/java -jar LocalProxy.jar >> proxy_log.log 2>&1 &", shell=True)
	while 1:
		done = False
		with open("proxy_log.log") as f:
			for line in f:
				if "active intermediate nodes: 1" in line:
					#tkMessageBox.showinfo("Done", "Startup sequence complete. You can run the experiment now.")
					done = True
					break
			if done: break

	os.chdir("../lp_compression/")
	os.system("sudo fuser -k 9090/tcp >> /dev/null 2>&1")
	os.system("rm -rf proxy_log.log")
	os.system("echo start >> proxy_log.log")
	subprocess.call("sudo /home/mooc/jre1.8.0_144/bin/java -jar LocalProxy.jar >> proxy_log.log 2>&1 &", shell=True)

	while 1:
		done = False
		with open("proxy_log.log") as f:
			for line in f:
				if "active intermediate nodes: 1" in line:
					tkMessageBox.showinfo("Done", "Startup sequence complete. You can run the experiment now.")
					done = True
					break
			if done: break

	print "Loaded. Starting User Info Collection"
	os.chdir("../")
	os.system("sudo python run_experiment.py &")
	master.destroy()

b = Button(master, text="Yes", command=show_url_list)
b.pack()

c = Button(master, text="No", command=master.quit)
c.pack()
mainloop()
