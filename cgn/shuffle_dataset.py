import sys
from random import shuffle

urls = []
with open(sys.argv[1], 'r') as f:
	for line in f:
		line = line.strip()
		if len(line) > 0:
			urls += [line.strip()]

shuffle(urls)

with open(sys.argv[2], 'w') as g:
	for url in urls[:50]:
		g.write(url + '\n')

