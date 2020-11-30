import sys
import json
import subprocess
from pprint import pprint
import os
import re

from viz_complete_time import img_diff

info = {}
info['with_compression_flag'] = False
info['exp_version'] = 1
info['cgn_node_location'] = 'ncalifornia'
info['url'] = sys.argv[3]
info['har_content'] = 'None'

with open('user_data.json') as f: data = json.load(f)

info['user_id'] = data['user_id']

def print_useage():
	print "Useage: " + sys.argv[0] + " <report path> --cgn_used=1/0 url number"	

if len(sys.argv) != 5: print_useage()
if "--cgn_used=" not in sys.argv[2]: print_useage()

cgn_used = int(sys.argv[2].split('=')[1].strip())
if cgn_used == 1: cgn_used = True
else: cgn_used = False

info['with_cgn_flag'] = cgn_used

path = sys.argv[1].strip()
if path[-1] != '/':
	path += '/'

# with open(path + 'perf.json') as f:
# 	data = json.load(f)
# 	info['timing_har'] = data

# with open(path + 'har.json') as f:
# 	data = json.load(f)
# 	info['general_har'] = data

# pprint(data)

# info['plt'] = float(int(data['domComplete']) - int(data['requestStart']))/1000.0

with open(path + 'vizComplete.log', 'r') as f:
	lines = f.readlines()
	info['viz_comp_90'] = lines[0].split(':')[1].strip().split(' ')[0].strip()
	info['viz_comp_80'] = lines[1].split(':')[1].strip().split(' ')[0].strip()
	info['plt'] = lines[2].split(':')[1].strip().split(' ')[0].strip()

with open('url_rtt_data.txt', 'r') as f:
	lines = f.readlines()
	if len(lines) > 0:
		info['rtt_cgn'] = lines[0].strip()
	else:
		info['rtt_cgn'] = '-1'

	if len(lines) > 1:
		info['rtt_webserver'] = lines[1].strip()
	else:
		info['rtt_webserver'] = '-1'

	if len(lines) > 2:
		info['ip_webserver'] = lines[2].strip()
	else:
		info['ip_webserver'] = '-1'

	try:
		os.remove("url_correctness.txt")
	except OSError:
		pass

	number = sys.argv[4]

	with open('current_url.har') as fp:
		har_data = json.load(fp)

	if int(number) % 2 == 0:
		info['with_compression_flag'] = True
	elif cgn_used:
		with open("./lp/proxy_log.log", 'r') as f:
			log = f.read()

		os.system("sudo truncate -s 0 ./lp/proxy_log.log")

		sizes = re.findall('#@#@[0-9]+.?[0-9]*#@#@', log)
		total = 0.0
		for s in sizes:
			total += float(s[4:-4])

		with open('current_url.har') as fp:
			data = json.load(fp)

		har_data['totalSize'] = total

	info['har_content'] = har_data

	if int(number) < 0:
	  	info['viz_correctness_80'] = '-1.0'
	  	info['viz_correctness_90'] = '-1.0'
	  	info['viz_correctness_plt'] = '-1.0'
	else:
		info['viz_correctness_80'] = str(img_diff(str(number) + '_nocgn/80viz.screenshot', str(number) + '_cgn/80viz.screenshot'))
		info['viz_correctness_90'] = str(img_diff(str(number) + '_nocgn/90viz.screenshot', str(number) + '_cgn/90viz.screenshot'))
		info['viz_correctness_plt'] = str(img_diff(str(number) + '_nocgn/plt.screenshot', str(number) + '_cgn/plt.screenshot'))

with open(path + 'url_data.json', 'w') as fp:
	json.dump(info, fp, sort_keys=True, indent=4)

with open(path + 'url_data.json', 'r') as fp:
	content = fp.read()
	pprint(content)
	subprocess.call("curl -H \"Content-Type: application/json\" -X POST -d \'" + content + "\' http://129.132.227.168:5555/exp/data", shell=True)
