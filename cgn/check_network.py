from pyping import ping
import os


def working_fine(url, num):
	IP = "NONE"
	LOCAL_PROXY_PATH = "./lp/"
	if int(num) % 2 == 0:
		LOCAL_PROXY_PATH = "./lp_compression/"
	CGN_NODE_LIST_PATH = LOCAL_PROXY_PATH + "intermediate_nodes.list"
	with open(CGN_NODE_LIST_PATH) as f:
		for line in f:
			#print line
			if ":5555" in line:
				IP = line.split('=')[1].split(':')[0].strip()
				break
	rtn = False

	if IP == "NONE":
		return False

	with open("url_rtt_data.txt", 'w') as f:
		r = ping(IP)

		if r.ret_code == 0:
			rtn = True
			f.write(r.avg_rtt + '\n')

		if "http://" in url:
			url = url.strip()[7:]
		if "/" in url:
			url = url.split('/')[0].strip()
			
		r = ping(url)

		if r.ret_code == 0:
			f.write(r.avg_rtt + '\n')
			f.write(r.destination_ip + '\n')
			rtn = True

		r = ping('google.com')

		if r.ret_code == 0:
			rtn = True

	return rtn

def restart_local_proxy():
	cmd = "cd {1} && sudo java -jar LocalProxy.jar"
	os.popen(cmd)