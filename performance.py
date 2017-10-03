### performance.py
#
# Authors: Sam Slate and Yuelin Liu
# Date: October 3rd, 2017
# Function:
#	A class that contains functions to
#	calculate and print various performance 
# 	metrics based on provided results
#

import os
import numpy as np
import matplotlib.pyplot as plt

class Performance:

	def __init__(self, seed_folder_path, exclude_seeds):
		# Create data structure to hold all information
		# Has the form of:
		# {disease: {test_gene: {'perc': percentage out of 100, 'rank: rank, 'outof': ranked out of}, ... }, . . .}
		self.all_info = {}

		### Variables for performance measurement ###
		# Store the total sum of percentages
		self.total_sum_perc = 0
		# Store the total sum of the rank
		self.total_sum_rank = 0
		# Store the total sum of the possible genes
		self.total_pos_genes = 0
		# Store the total number of tests
		self.num_tests = 0
		# Store the total number of percentages that are less than .5
		self.num_less_point5_perc = 0
		# Store the total number of percentages that are less than 1
		self.num_less_1_perc = 0
		# Store the total number of percentages that are less than 5
		self.num_less_5_perc = 0

		# Sets local exclude_gene boolean to what was passed in
		self.exclude_seeds = exclude_seeds 

		# Calls the read in function
		self.read_in(seed_folder_path)
		
	# Reads in all of the data
	def read_in(self, seed_folder_path):
		# Retrieves all of the folders stored in the folder path
		dfolders = os.listdir(seed_folder_path)
		# Loops through each disease folder in SeedFiles
		for disease in dfolders:
			# Sets up disease info dictionary
			self.all_info[disease] = {}
			# Gets all of the files from the disease folder
			disease_path = seed_folder_path + "/" + disease
			allfiles = os.listdir(disease_path)
			# Call read in disease
			self.read_in_disease(disease, disease_path, allfiles)

	def read_in_disease(self, disease, disease_path, allfiles):
		print "Calculating disease: " + disease

		# Determine the number of seed genes by dividing the number
		# of files by 3
		num_seed_genes = len(allfiles)/3
		# Loop through the number of seed genes, offset by 1
		for g_i in range (1, num_seed_genes + 1):
			# Determine the file names corresponding to the index
			seedfile = disease + "_seed" + str(g_i) + ".txt"
			test_genefile = disease + "_test_gene" + str(g_i) + ".txt"
			rankfile = "seed" + str(g_i) + "_rank.txt"
				
			# Open the gene ranking file
			with open(disease_path + "/" + rankfile, 'r') as generankf:
				generank  = [line[:-1].split('\t') for line in generankf]
				generank  = [x[0] for x in generank]

			# Open the single gene file
			with open(disease_path + "/" + test_genefile, 'r') as singlegenef:
				genetorank = singlegenef.read().split('\t')[0]
				genetorank = genetorank.replace('\n', '')

			# Open the file of genes to be excluded
			with open(disease_path + "/" + seedfile, 'r') as genesexcludedf:
				genesexcluded  = [line.split('\t')[0] for line in genesexcludedf]
				genesexcluded = [gene.replace('\n', '') for gene in genesexcluded]
				genesexcludedf.close()

			# Call calculate_data
			self.calculate_data(disease, generank, genetorank, genesexcluded)

	def calculate_data(self, disease, generank, genetorank, genesexcluded):
		if self.exclude_seeds:
			# Excludeds the seed genes from the ranking
			generank = [gene for gene in generank if gene not in genesexcluded]
		# Calculates the rank number
		rank= generank.index(genetorank) + 1

		# Calculates the percentage
		perc = float(rank)/float(len(generank))
		# Adds to total before it is rounded for better accuracy
		self.total_sum_perc += perc
		# If less than .5, increment
		if perc < .005: self.num_less_point5_perc += 1
		# If less than 1, increment
		if perc < .01: self.num_less_1_perc += 1
		# If less than 5, increment
		if perc < .05: self.num_less_5_perc += 1
		# Rounds the percentage to two decimal places
		perc *= 100 

		# Add all of the information the to data structure
		self.all_info[disease][genetorank] = {'perc': perc, 'rank': rank, 'outof': len(generank)}

		# Adds to totals
		self.num_tests += 1
		self.total_sum_rank += rank
		self.total_pos_genes += len(generank)

	def print_detailed(self):
		# Loop through disease
		for disease, genes in self.all_info.items():
			print(disease + ":\n")
			# Loop through test genes
			for gene, i in genes.items():
				rank_statement = "The rank for " + str(gene) + " is: " + str(i['rank']) + " out of " + str(i['outof']) + "\n"
				perc_statement = "The percentage is: " + str(i['perc']) + "%\n\n"
				print(rank_statement)
				print(perc_statement)

	def print_total_info(self):
		# Print total info
		statement = ""
		statement += "The average rank number was " + str(float(self.total_sum_rank)/float(self.num_tests))
		statement += " out of an average of " + str(float(self.total_pos_genes)/float(self.num_tests)) + " possible genes\n"
		statement += "The average percentage was " + str(float(self.total_sum_perc)/float(self.num_tests) * 100) + "%\n"
		statement += "The percentage of true genes that were ranked in the top .5% was " + str(float(self.num_less_point5_perc)/float(self.num_tests) * 100) + "\n"
		statement += "The percentage of true genes that were ranked in the top 1% was " + str(float(self.num_less_1_perc)/float(self.num_tests) * 100) + "\n"
		statement += "The percentage of true genes that were ranked in the top 5% was " + str(float(self.num_less_5_perc)/float(self.num_tests) * 100) + "\n"
		statement += "The total average of the average percentage for each disease was " + str(self.get_avg_of_avgs()) 
		print statement

	def print_disease_sizes(self):
	# Loop through diseases
		for disease, genes in self.all_info.items():
			# Print out disease and its size
			print disease + "\t" + str(len(genes))


	def get_avg_of_avgs(self):
		# List that contains the averages for each diseases
		avgs = []
		# Loop through diseases
		for disease, genes in self.all_info.items():
			# Contains the current sum of all of the percentages in that disease
			perc_sum = 0
			# Loops through the genes in the disease
			for gene, info in genes.items():
				# Add the percentage to perc_sum
				perc_sum += info['perc']
			# Adds the average percent for that disease to the list of averages
			avgs.append(float(perc_sum)/float(len(genes)))

		# Calculate the averages of the averages and store it in self
		self.avg_of_avgs = float(sum(avgs))/float(len(avgs))
		return self.avg_of_avgs

	def print_dif_d_avg_to_avg_of_avgs(self):
		# Loop through diseases
		for disease, genes in self.all_info.items():
			# Contains the current sum of all of the percentages in that disease
			perc_sum = 0
			# Loops through the genes in the disease
			for gene, info in genes.items():
				# Add the percentage to perc_sum
				perc_sum += info['perc']
			# Calculates the average percent for that disease
			avg_perc = float(perc_sum)/float(len(genes))
			# Prints out the difference between the avgerage percent for the disease
			# and the avg of averages
			print str(disease) + "\t" + str(avg_perc - self.avg_of_avgs) 


	def print_simple(self):
		print ("Disease\tGene\tRank\tOut of\tPercentage")
		# Loop through diseases and genes
		for disease, genes in self.all_info.items():
			for gene, i in genes.items():
				# Calculate each percentage and print
				perc = int(float("{0:.2f}".format(i['perc'])))
				print(disease + "\t" + str(gene) + "\t" + str(i['rank']) + "\t" + str(i['outof']) + "\t" + str(i['perc']))

	def print_all_percents(self):
		# Loops through diseases and genes
		for disease, genes in self.all_info.items():
			for gene, i in genes.items():
				# Calculates the percentage
				perc = int(float("{0:.2f}".format(i['perc'])))
				print(perc)

	def print_perc_histo(self):
		# Stores the number of times each percentage shows up
		num_range = [0] * 101

		# Loops through diseases and genes
		for disease, genes in self.all_info.items():
			for gene, info in genes.items():
				# Increments the spot in num_range for the percentage by 1
				perc = int(float("{0:.2f}".format(info['perc'])))
				num_range[perc] += 1

		# Prints each percentage and frequency
		print("Percentage\tFrequency")
		for i, num in enumerate(num_range):
			print(str(i) + "\t" + str(num))


	def print_range_per_dis_histo(self):
		# Store the number of times each range shows up
		num_range = [0] * 101

		# Loops through diseases and genes
		for disease, genes in self.all_info.items():
			# Store all of the percentages for that disease
			all_percs = [info['perc'] for gene, info in genes.items()]
			# Find the range
			p_range = max(all_percs) - min(all_percs)
			p_range = int(float("{0:.2f}".format(p_range)))
			num_range[p_range] += 1

		# Print ranges
		print("Percentage Range\tFrequency")
		for i, num in enumerate(num_range):
			print(str(i) + "\t" + str(num))

	def print_avg_perc_size(self):
		# Dictionary to store the size of a disease as a key and a list
		# of sum percentage and number of seeds in a disease with that size
		dict_info = {}
		for disease, genes in self.all_info.items():
			# gGet size
			size = len(genes)
			# If size is not in the dict, add it and initailize it
			if size not in dict_info:
				dict_info[size] = [0, 0]
			# Size number of seeds to the seed counter
			dict_info[size][1] += size
			# Loop through the test genes and add the percentages to the sum
			for gene, info in genes.items():
				dict_info[size][0]+=info['perc']

		# Tturn the dict into a list and sort it by the key
		list_info = [[size,info] for size, info in dict_info.items()]
		list_info.sort(key=lambda x: x[0])

		#print headers
		print("Size of Disease\tAverage Percentile\tNumber Disease\tNumber Genes")

		# Calculate and print 
		for pair in list_info:
			perc = float(pair[1][0])/float(pair[1][1])
			perc = int(float("{0:.2f}".format(perc))) 
			print(str(pair[0]) + "\t" + str(perc) + "\t" + str(pair[1][1]/pair[0]) + "\t" + str(pair[1][1]))

	def perc_above_thresh(self, thresh):
		# Initialize sum variables
		outof = 0
		total = 0

		# Loop through each disease
		for disease, genes in self.all_info.items():
			# Add the length of genes to outof
			outof += len(genes)
			# Loop through the test genes
			for gene, info in genes.items():
				# Test to see if the rank is within threshold
				if info['rank'] <= thresh:
					# If so, increment total
					total += 1

		# Calculate the percentage and print
		perc = 100 * float(total)/float(outof)
		return perc

	def get_cowen_roc(self):
		# Set the max threshold
		max_thresh = 500

		# Initialize a list to hold the percentages at each threshold
		perc_at_thresh = [0] * max_thresh

		# Loop through each threshold
		for thresh in range(0, max_thresh):
			perc_at_thresh[thresh] = self.perc_above_thresh(thresh)

		return perc_at_thresh

	def auc (self, plot):
		# Calculate area under the curve
		sum = plot[0] + plot[-1]
		for num in plot[1:(len(plot) - 1)]:
			sum = float(sum) + 2 * num
		return float(sum)/float(2)

	def make_cowen_ROC_graph(self, filename):
		# Create graph using plt on the array created by get_cowen_roc
		plt.plot(self.get_cowen_roc())
		plt.ylabel('Percentage Above Rank Threshold')
		plt.xlabel('Rank Threshold')
		plt.savefig(filename + '.cowen_ROC.png')

	def print_cowen_ROC(self):
		# Print ROC information
		print("Rank Threshold\tPercentage Above Rank Threshold")
		for thresh, perc in enumerate(self.get_cowen_roc()):
			print str(thresh) + "\t" + str(perc)


	def get_auc(self):
		# Return the AUC
		return self.auc(self.get_cowen_roc())
