### pool_with_closure.py
#
# Authors: Sam Slate and Yuelin Liu
# Date: October 3rd, 2017
# Function:
#	A script that runs another 
#	multiprocessing script defined
#	by a function and closure template
# 	on a given set of input using
#	python's multiprocessing library

from multiprocessing import Pool
import time
import os
import sys

## ** Change to relevant file ** ##
from mp_combine import *

# Defines the number of cores used
number_cores = 32
# Whether or not to use the old method
old_method = False

if __name__ == "__main__":

	#### Seed File Related ####

	print "Reading in seed folder"
	# Get the seed folder path from the argument
	seed_folder_path = sys.argv[1]
	# Add a forward slash if there is not one already
	if seed_folder_path[-1] != "/":
			seed_folder_path += "/"
	
	# Retrieve all of the disease folders
	dfolders = os.listdir(seed_folder_path)

	# List to hold all of the paths of all of the seed files 
	seed_file_paths = []

	# Loop through disease folders in dfolders
	for dfolder in dfolders:
		# Retreieve all of the files
		allfiles = os.listdir(seed_folder_path + dfolder)
		# Add the seed file paths to seed_files_paths
		seed_file_paths += [seed_folder_path + dfolder + "/" + f for f in allfiles if "_seed" in f]

	print "Finished reading in seed folder"

	#### Serial Processing ####

	# Checks to see if should run serial processing
	if old_method:
		print "Starting serial processing"

		# Get the time at the start
		t1 = time.time()
		# Get the number of seed file paths
		length = len(seed_file_paths)
		# Loop through them
		for i, x in enumerate(seed_file_paths):
			print "Calculating: " + str(i) + " out of " + str(length)
			# Run the function on the seed_file_path
			mp_func((x, closure_to_pass))

		# Get the time at the end and calculate the diference
		sptime = time.time() - t1

		print "Ending serial processing"

	#### Pool Processing ####

	if not old_method:

		print "Starting pool processing"

		# Create list of pairs of seed file paths and the closure
		paths_and_closure = [[p, closure_to_pass] for p in seed_file_paths]

		# Get the time at the start
		t2 = time.time()
		# Create a pool with the number of cores defined above
		p = Pool(processes=number_cores)
		# Map the function on the seed file paths and closure and catch the result (there shouldn't be one)
		result = p.map(mp_func, paths_and_closure)
		# Close the pool
		p.close()
		# Join the pool
		p.join()

		# Get the time at the end and calculate the diference
		pptime = time.time() - t2

		print "Ending pool processing"

	#### Final Print Out ####

	# Only print serial processing time if old method is true
	if old_method:
		print "Serial processing took: " + str(sptime)
	if not old_method: 
		print "Pool took: " + str(pptime)


