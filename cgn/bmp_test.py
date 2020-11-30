import argparse
import urlparse
import sys
import os
import subprocess
import collections
import textwrap

from pyvirtualdisplay import Display
import pyscreenshot as ImageGrab

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import threading

import json


from browsermobproxy import Server

bypass_list = "https,google,gstatic,.youtube.,cloudfront,s3.amazonaws,images-amazon,media-imdb,.ytimg.,akamai,.files.,analytics,static,.woff,.woff2,.ttf,cdn,443:"


class VisualCompletion:
	def __init__(self, args):

		#if args['xcompression']:
		#	PROXY = "127.0.0.1:9090"
		#else:
		#	PROXY = "127.0.0.1:8080" # IP:PORT or HOST:PORT

		# bmp_path = os.getenv('BROWSERMOB_PROXY_PATH', './browsermob-proxy-2.1.2/bin/browsermob-proxy')
		# self.bmp_server = Server(bmp_path, {'port':9001})
		# self.bmp_server.start()
		# self.bmp_proxy = self.bmp_server.create_proxy()
		
		# url = urlparse.urlparse (self.bmp_proxy.proxy).path

		#chrome_options = webdriver.ChromeOptions()
		# chrome_options.add_argument("--proxy-server={0}".format(url))
		#chrome_options.add_argument("--no-sandbox")
		#if args['cgn']: 
		#	print "::: Enabling Proxy = 127.0.0.1:8080 :::"
		#	chrome_options.add_argument('--proxy-server=%s' % PROXY)
			#chrome_options.add_argument('--proxy-bypass-list=\"{0}\"'.format(bypass_list))

		#if args['flywheel']: chrome_options.add_extension("./extension_2_0_2.crx")

		#if args['adblock']: chrome_options.add_extension("./extension_1_13_2.crx")

		#chromedriver = os.getenv("CHROMEDRIVER_PATH", "./chromedriver")

		if args['cgn']:	
			print "FIReFOX PROFILE : HERE"	
			profile = webdriver.FirefoxProfile()
			profile.set_preference("network.proxy.type", 1)
			profile.set_preference("network.proxy.http", "127.0.0.1")

			if args['xcompression']:
				profile.set_preference("network.proxy.http_port", 9090)
			else:
				profile.set_preference("network.proxy.http_port", 8080)
				profile.set_preference("network.proxy.no_proxies_on", bypass_list)

			profile.update_preferences() 
		else:
			profile = webdriver.FirefoxProfile()
			profile.set_preference("network.proxy.type", 0)
			profile.update_preferences() 

		self.chrome = webdriver.Firefox(firefox_profile=profile)

                self.chrome.set_page_load_timeout(60)

		self.screenshot_count = 0
		self.finished = False

		self.take_screenshot(args)

		# self.bmp_proxy.new_har(args['url'], options={'captureHeaders': True})
		
		try:
                        self.chrome.get(args['url'])
                except:
                        self.chrome.close()
                        exit()

		self.finished = True

		from datetime import datetime
		print "%s: Finish"%(datetime.now())

		# result = json.dumps(self.bmp_proxy.har, ensure_ascii=False)

		# performance = json.dumps(self.chrome.execute_script("return window.performance"), ensure_ascii=False)

		# with open(args['path']+'/'+ 'har' + '.json', 'w') as har_file:
			# har_file.write(str(result))

		# with open(args['path']+'/'+ 'perf' + '.json', 'w') as har_file:
			# har_file.write(str(performance))

		# self.bmp_server.stop()

		with open('current_url.har', 'w') as fp:
			json.dump(dict(self.get_event_times()), fp)

		self.chrome.close()

		#chrome.get("http://whatismyipaddress.com")

	def inject_timing_js(self):
		self.jscript = textwrap.dedent("""
		    var performance = window.performance || {};
		    var timings = performance.timing || {};
		    return timings;
		    """)
		timings = self.chrome.execute_script(self.jscript)
		return timings

	def get_event_times(self):
		timings = self.inject_timing_js()
		good_values = [epoch for epoch in timings.values() if epoch != 0]
		ordered_events = ('navigationStart', 'fetchStart', 'domainLookupStart',
				  'domainLookupEnd', 'connectStart', 'connectEnd',
				  'secureConnectionStart', 'requestStart',
				  'responseStart', 'responseEnd', 'domLoading',
				  'domInteractive', 'domContentLoadedEventStart',
				  'domContentLoadedEventEnd', 'domComplete',
				  'loadEventStart', 'loadEventEnd'
				  )
		event_times = ((event, timings[event] - min(good_values)) for event
			       in ordered_events if event in timings)
		return collections.OrderedDict(event_times)

	# Muhammad
	def take_screenshot(self, args):
		if self.finished: 
			print "Ending"
			return

		interval = 0.2
		if 'time' in args:
			interval = float(args['time'])

		threading.Timer(interval, self.take_screenshot, [args]).start()

		if 'path' in args:
			prefix = args['path'] + '/'
		else:
			prefix = ''

		# if self.display:
		# 	self.display.waitgrab().save(prefix + str(self.screenshot_count) + ".png", "PNG")
		# else:
		# 	ImageGrab.grab().save(prefix + str(self.screenshot_count) + ".png", "PNG")

		ImageGrab.grab().save(prefix + str(self.screenshot_count) + ".png", "PNG")		

		self.screenshot_count += 1

		if (self.screenshot_count > 300):
			print "Timed out. Moving to next url."
			self.finished = True
			exit()


if __name__ == '__main__':
	# for headless execution
	#with Xvfb() as xvfb:
	parser = argparse.ArgumentParser(description='Performance Testing using Browsermob-Proxy and Python')
	parser.add_argument('-u','--url',help='URL to test',required=True)
	parser.add_argument('-p','--path',help='Select path for output files',required=False)
	parser.add_argument('-f', '--flywheel', help='Use Google FlyWheel', required=False)
	parser.add_argument('-H', '--headless', help='Run headlessly', required=False)
	parser.add_argument('-a', '--adblock', help='Block Ads', required=False)
	parser.add_argument('-t', '--time', help='Time interval for visual completeness calculations', required = False)
	parser.add_argument('-c', '--cgn', help='Use CGN Node', required=False)
	parser.add_argument('-x', '--xcompression', help='Use Compression', required=False)
	args = vars(parser.parse_args())

	display = None
	if args['headless']:
		#display = SmartDisplay(visible=0)
		display = Display(visible=0, size=(1024, 768))
		display.start()

	RUN = VisualCompletion(args)
	#display.quit()
	print "END"
