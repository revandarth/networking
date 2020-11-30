import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

count = 0
while count < 5:
	profile = webdriver.FirefoxProfile()
	profile.add_extension("har_export_trigger-0.5.0-beta.7-fx.xpi")

	#set firefox preferences
	profile.set_preference("app.update.enabled", 0)
	domain = "devtools.netmonitor.har."

	#set the preference for the trigger
	profile.set_preference("extensions.netmonitor.har.contentAPIToken", "test")
	profile.set_preference("extensions.netmonitor.har.autoConnect", True)
	profile.set_preference(domain + "enableAutoExportToFile", True)
	profile.set_preference(domain + "defaultLogDir", "/home/cgn/")
	#profile.set_preference(domain + "pageLoadedTimeout", 1500)

	time.sleep(2)

	#create firefox driver
	driver = webdriver.Firefox(profile)
	driver.get("https://www.python.org")
	count=count+1
	time.sleep(2)

	#close the firefox driver after HAR is written
	driver.close()