### mp_combine.py
#
# Authors: Sam Slate and Yuelin Liu
# Date: October 3rd, 2017
# Function:
#	A script based on the multi-processing template that
#	combines two rankings to produce a third based on 
#	given biases and combination methods
#
#

import os

## ** Add global variables here, they will be included ** ##

# Whether or not to multiply instead of add the ranks
multiply_instead_of_add = False

# Bias of ranking towards method 1, out of 100. 100 is just method 1, 
# 0 is just method 2, 50 is weighted equally
bias_towards_1 = 50
# The bias towards 2 is 100 minus the bias towards 1
bias_towards_2 = 100 - bias_towards_1

# The seed directory that has the rankings for method 1
meth_1_dir_path = '/r/bcb/lily_sam_summer_2017/SeedDirectories/MIPS_yeast/stringdb/RWR_set1_rp0.9_stringdb/'
# The seed directory that has the rankings for method 2
meth_2_dir_path = '/r/bcb/lily_sam_summer_2017/SeedDirectories/MIPS_yeast/stringdb/avg_cDSD_step1_set1_stringdb/'
# The seed directory that will hold the results
result_dir_path = '/r/bcb/lily_sam_summer_2017/SeedDirectories/MIPS_yeast/stringdb/combo_add_50_RWR_.9_avg_cDSD_1_set1_stringdb/'


## ** Define closure dictionary here, will be imported and passed into mp_func ** ##
closure_to_pass = {
	## ** Add here ** ##
}

# ** Name and contract of the function must stay the same:
# **	Argument: a tuple in the format of (seed_file_path, closure)
# **	Returns : nothing
def mp_func(pair_seed_file_path_closure):

	## ** Useful strings and functions I'm giving to you :) ** ##

	# Get the seed_file_path
	seed_file_path = pair_seed_file_path_closure[0]
	# Get the closure
	closure = pair_seed_file_path_closure[1]

	# Get the disease path
	disease_path = '/'.join(seed_file_path.split("/")[:-1]) + "/"
	# Get the disease name
	disease_name = seed_file_path.split("/")[-2] 
	# Get the seed file name
	seed_file_name = seed_file_path.split("/")[-1]
	# Get the rank file name
	rank_file_name = 'seed' + seed_file_name.split('seed')[1][:-4] + "_rank.txt"

	# Get the rank file path
	rank_file_path = disease_path + rank_file_name

	## ** Write your code here! ** ##

	print seed_file_path
	# Opens the method 1 ranking file
	with open(meth_1_dir_path + disease_name + '/' + rank_file_name, 'r') as meth_1_f:
		# Special case for RWR files 
		if "RWR" in meth_1_dir_path:
			meth_1_ranks = [line.split('\t')  for line in meth_1_f]
			meth_1_ranks = [x[0] for x in meth_1_ranks]
		else:
			# Creates list of gene name in order they are ranked
			meth_1_ranks = meth_1_f.read().splitlines()

	# Opens the method 1 ranking file
	with open(meth_2_dir_path + disease_name + '/' + rank_file_name, 'r') as meth_2_f:
		# Special case for RWR files 
		if "RWR" in meth_2_dir_path:
			meth_2_ranks = [line.split('\t')  for line in meth_2_f]
			meth_2_ranks = [x[0] for x in meth_2_ranks]
		else:
			# Creates list of gene name in order they are ranked
			meth_2_ranks = meth_2_f.read().splitlines()

	# A list of tuples containing a gene and its calculated score
	gene_scores = []

	# Loops through the genes in meth_1_rank
	for index, gene in enumerate(meth_1_ranks):
		# Gets the rank of the gene from method 1 by adding 1 to the index
		# (we don't want the first ranked gene to have a rank of 0)
		meth_1_rank = index + 1
		# Gets the rank of the gene from method 2 by adding 1 to the index
		meth_2_rank = meth_2_ranks.index(gene) + 1

		# Calculate the weights for each method by multiplying by the bias
		meth_1_weight = (meth_1_rank * bias_towards_1)
		meth_2_weight = (meth_2_rank * bias_towards_2)

		# Check if should use multiplication
		if multiply_instead_of_add:
			# If so, calculate the score by multiplying the weights
			score = meth_1_weight * meth_2_weight
		else:
			# If not, calculate the score by adding the weights
			score = meth_1_weight + meth_2_weight

		# Adds the score to gene_scores
		gene_scores.append((gene, score))

	# Sorts the gene_scores
	gene_scores.sort(key = lambda x : x[1])

	## Break ties using the first method ##

	# Group the ranking by scores and create a list of lists in the form
	# of: [[gene1, gene2, gene3], [gene4, gene5], [gene6], ...]
	rank_by_score = []
	# Store the current score
	cur_score = -1
	# Loop through every rank pair
	for gene_score_pair in gene_scores:
		# Check if the score is equal to the current score
		if gene_score_pair[1] == cur_score:
			# If so, append the gene to the last list in rank_by_score
			rank_by_score[-1].append(gene_score_pair[0])
		else:
			# If not, update the new rank to be the current rank
			cur_score = gene_score_pair[1]
			# Append a new list to tie_rank_by_score with the rank as its only value
			rank_by_score.append([gene_score_pair[0]])

	## Sorting rank_by_score
	# Sort each individual gene list by its index in the method 1 rank list
	tie_rank_by_score_sorted = [sorted(gene_list, key = lambda x: meth_1_ranks.index(x)) for gene_list in rank_by_score]

	# Flatten tie_rank_by_score_sorted
	new_rank = [item for sublist in tie_rank_by_score_sorted for item in sublist]

	# Oopen the ranking file in the results directory
	with open(result_dir_path + disease_name + '/' + rank_file_name[:-9] + '_rank' + '.txt', 'w') as r:
		# Loop through tie_rank_by_score_sorted
		for gene in new_rank:
				r.write(str(gene) + '\n')
