import subprocess
import sys
import os
import json
import Tkinter as tk
import uuid
import subprocess

def generate_gui():
	info = {}

	root = tk.Tk()
	root.title("Content Gathering Network Pipeline v1.0")

	master = tk.Frame(master=root)
	master.grid(sticky=tk.N + tk.S + tk.E + tk.W)

	frame_one = tk.LabelFrame(master, text="Your Information", padx=5, pady=5)
	frame_one.grid()

	frame_two = tk.LabelFrame(master, text="Experiment", padx=5, pady=5)
	frame_two.grid()

	tk.Label(master, text="What is your current country?").grid(row=0, in_=frame_one)
	tk.Label(master, text="What is your state/canton/province?").grid(row=1, in_=frame_one)
	tk.Label(master, text="What is your current city?").grid(row=2, in_=frame_one)
	tk.Label(master, text="ISP (Type \'unknown\' if you don't know)").grid(row=3, in_=frame_one)
	tk.Label(master, text="Connection Type (click to change)").grid(row=4, in_=frame_one)
	tk.Label(master, text="What is your upload bandwidth? (in Mbps)").grid(row=5, in_=frame_one)
	tk.Label(master, text="What is your download bandwidth? (in Mbps)").grid(row=6, in_=frame_one)
	tk.Label(master, text="What are your monthly ISP charges? (in USD)").grid(row=7, in_=frame_one)

	e1 = tk.Entry(master)
	e4 = tk.Entry(master)
	e2 = tk.Entry(master)
	e3 = tk.Entry(master)

	var = tk.StringVar(master)
	var.set("Dial-up")

	e5 = tk.OptionMenu(master, var, "Cable", "DSL/ADSL - ISDN", "Fiber-to-the-home", "Wireless Broadband", "Mobile/cellular network", "Satellite", "University/company network", "Public Wifi", "Other")

	e6 = tk.Entry(master)
	e7 = tk.Entry(master)
	e8 = tk.Entry(master)

	e3.insert(10, "unknown")
	#e5.insert(10, "unknown")
	e6.insert(10,"unknown")
	e7.insert(10,"unknown")
	e8.insert(10,"unknown")

	e1.grid(row=0, column=1, in_=frame_one)
	e4.grid(row=1, column=1, in_=frame_one)
	e2.grid(row=2, column=1, in_=frame_one)
	e3.grid(row=3, column=1, in_=frame_one)
	e5.grid(row=4, column=1, in_=frame_one)
	e6.grid(row=5, column=1, in_=frame_one)
	e7.grid(row=6, column=1, in_=frame_one)
	e8.grid(row=7, column=1, in_=frame_one)

	frame = 0

	def update_user_info():
		info['user_country'] = e1.get().lower()
		info['user_city'] = e2.get().lower()
		info['user_state'] = e4.get().lower()
		info['user_isp'] = e3.get().lower()
		info['user_id'] = str(uuid.uuid1())
		info['user_connection'] = var.get().lower()
		info['user_upload'] = e6.get().lower()
		info['user_download'] = e7.get().lower()
		info['user_price'] = e8.get().lower()
		info['exp_version'] = 1

		os.system("sudo curl whatismyip.akamai.com > my_ip.txt")

		with open("my_ip.txt", 'r') as fp:
			info['client_ip'] = fp.read()

		with open('user_data.json', 'w') as fp:
			json.dump(info, fp, sort_keys=True, indent=4)

		with open('user_data.json', 'r') as fp:
			content = fp.read()
			subprocess.call("curl -H \"Content-Type: application/json\" -X POST -d \'" + content + "\' http://129.132.227.168:5555/exp/user", shell=True)			
		
		exp_time = slider.get()
		root.destroy()

		print "*" * 10
		print "Running Experiment"
		print "*" * 10

		subprocess.call("sudo python test_urls.py url_list.txt " + str(exp_time) + " --handleproxy", shell=True)
		subprocess.call("sudo rm -rf [0-9]*_*cgn", shell=True)

	valuelist = [x * 10 for x in range(1,13)]

	def valuecheck(value):
		newvalue = min(valuelist, key=lambda x:abs(x-float(value)))
		slider.set(newvalue)

	tk.Label(master, text="How much time (in minutes) will you contribute to the experiment?").grid(row=3, pady=4, in_=frame_two)

	slider = tk.Scale(master, from_=min(valuelist), to=max(valuelist), command=valuecheck, tickinterval=10, orient="horizontal", length=400)
	slider.set(60)
	slider.grid(row=4, column=0, in_=frame_two)

	tk.Button(master, text="Run Experiment", command=update_user_info).grid(row=5, column=0, columnspan=2, pady=4, in_=frame_two)

	tk.Button(master, text="Quit", command=master.quit).grid(row=6, column=0, pady=4)

	#tk.Button(master, text="Show URL List", command=show_url_list).grid(row=5, column=0, sticky=tk.E, pady=4, in_=frame_two)

	tk.mainloop()


if __name__ == '__main__':
	generate_gui()
