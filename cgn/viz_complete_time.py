from itertools import izip
from PIL import Image
import argparse
import glob
import sys
from shutil import copy2

def count_images(args):
	images = glob.glob(args['path'] + '/*.png')

	formatted_images = []
	for i in images:
		formatted_images.append(int(i.split('/')[-1][:-4]))

	return str(sorted(formatted_images)[-1])

def img_diff(i1dir, i2dir):
	i1 = Image.open(i1dir)
	i2 = Image.open(i2dir)

	assert i1.mode == i2.mode, "Different kinds of images."
	assert i1.size == i2.size, "Different sizes."
	 
	pairs = izip(i1.getdata(), i2.getdata())
	if len(i1.getbands()) == 1:
	    # for gray-scale jpegs
	    dif = sum(abs(p1-p2) for p1,p2 in pairs)
	else:
	    dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
	 
	ncomponents = i1.size[0] * i1.size[1] * 3
	return (dif / 255.0 * 100) / ncomponents

def viz_complete_time(args):
	x = float(args['percentage'])
	t = 0
	i = 0

	num_img = count_images(args)
	print "Number of images:", num_img

	base_diff = img_diff(args['path'] + '/' + str(i) + '.png', args['path'] + '/' + num_img + '.png')
	pdiff = 100

	lower_time = -1

	while (pdiff >= 100 - x):

		if (args['lowermetric']):
			if (pdiff < 100 - (x - 10)) and lower_time < 0:
				lower_time = t
				copy2(args['path'] + '/' + str(i) + '.png', args['path'] + '/' + '80viz.screenshot')
				

		if i > int(num_img):
			print "\nSomething weird happened. Apparently it never reaches that similarity."
			exit()

		sys.stdout.write("\rOn {0}th image. Processing {1:.2f} % done".format(str(i), i * 100.0/float(num_img)))
		sys.stdout.flush()

		i += 1
		t += float(args['time'])

		old_pdiff = pdiff

		try: pdiff = img_diff(args['path'] + '/' + str(i) + '.png', args['path'] + '/' + num_img + '.png') * 100.0 / base_diff
		except:
			pdiff = old_pdiff
		
	print ""

	if lower_time < 0.0:
		lower_time = t
		copy2(args['path'] + '/' + str(i) + '.png', args['path'] + '/' + '80viz.screenshot')

	copy2(args['path'] + '/' + str(i) + '.png', args['path'] + '/' + '90viz.screenshot')
	copy2(args['path'] + '/' + num_img + '.png', args['path'] + '/' + 'plt.screenshot')
	return t, float(args['time']) * float(num_img), lower_time

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Implementation of Visual Completeness Time')
	parser.add_argument('-p','--path',help='Select path for input files',required=True)
	parser.add_argument('-t','--time',help='Time interval between images in seconds',required=True)
	#parser.add_argument('-n','--numimg',help='Number of images', required=True)
	parser.add_argument('-x','--percentage',help='Cutoff percentage', required=True)
	parser.add_argument('-l', '--lowermetric', help='Record 10\% less than cutoff', required=False)
	args = vars(parser.parse_args())

	rtn, plt, lower_t = viz_complete_time(args)
	print args['percentage'], "% Visual Completeness Time:", rtn, "seconds"
	print float(args['percentage']) - 10, "% Visual Completeness Time:", lower_t, "seconds"
	print "Page Load Time", plt, "seconds"

	with open(args['path'] + '/' + 'vizComplete.log', 'w') as f:
		f.write("{0} % visual completeness: {1} seconds\n".format(args['percentage'], str(rtn)))
		f.write("{0} % visual completeness: {1} seconds\n".format(str(float(args['percentage'])-10), str(lower_t)))
		f.write("PLT: {0} seconds".format(str(plt)))
