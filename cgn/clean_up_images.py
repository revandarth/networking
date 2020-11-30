import glob
import os
import argparse 

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Cleans up PNG files in a directory')
	parser.add_argument('-p','--path',help='Select path for input files',required=True)

	args = vars(parser.parse_args())

	print "Removing PNG files..."
	files = glob.glob(args['path'] + '/*.png')

	for f in files:
		os.remove(f)

	print "Files removed"

