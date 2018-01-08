# DSD (Diffusion State Distance) Phenotype Ranking Example Code
### By Sam Slate and Yuelin Liu
Example code for research project on ranking for phenotype relevances based on the diffusion state distance. Poster accepted to Computational Aspects of Biological Information (CABI) 2017.

# Abstract and poster describing our research
The Diffusion State Distance metric (DSD), introduced by Cao et al. in 2013, has been shown to improve existing methods for function prediction and community detection in protein-protein interaction networks. Diffusion-based methods have also been used extensively in gene prioritization, where the goal is, given a set of genes known to be associated a disease or phenotype, to use network information to rank a set of candidate genes by their likelihood to share relevance with the disease or phenotype. Therefore, we asked whether DSD-based methods were superior to standard ranking methods such as random walk with restart (RWR) for this problem, as well. We considered both a set of disease phenotypes from OMIM in the human network, and sets of trait phenotypes from GO terms of sufficient specificity and MIPS in Baker’s yeast. We compared 1) average target gene ranking, 2) percentage of target genes ranked within the top 5%, 1%, and 0.5%, and 3) area under the initial portion of the ROC curve using DSD-variants, each using different length random-walks, and RWR in stringent leave-one-out cross validation experiments. The DSD algorithms all performed worse when the length of the random walk was longer; with short random walks, DSD performed comparably to RWR. Hybrid algorithms, however, that ranked based on the weighted sum and weighted product of rankings obtained from RWR and short random walk DSD outperformed either one alone. We conclude that diffusion-based methods for gene prioritization seem more locality sensitive than for function prediction or community detection. 


<img src="https://github.com/sam-slate/dsd-phenotype-ranking-example-code/blob/master/FinalPoster.jpg?raw=true" alt="File Structure" style="width:304px">


# Files

## [performance.py](https://github.com/sam-slate/dsd-phenotype-ranking-example-code/blob/master/performance.py)
### Purpose:
A class that contains functions to calculate and print various performance metrics based on provided results
### Lower level description:
A python class that has three basic functionalities:
- **Read in and store data:**
  - Parses and cleans data
  - Creates a data structure in the form of: 
  ```python
  {disease: {test_gene: {'perc': percentage out of 100, 'rank: rank, 'outof': ranked out of}, ... }, . . .} 
  ```
  - Sorts the data into the data structure
- **Calculate performance metrics:**
  - Implements basic metric calculations by looping through the above data structure and performing calculations
  - Stores important information in the class to reuse for various metrics
  - Implements AUC (Area Under the Curve) calculations for a specialized ROC (Receiver Operating Characteristic) using basic calulus formulas and modularity
- **Print performance metrics:**
  - Parses and prints the results from various metrics using string manipulation

### Concepts used:
- Object oriented programming and modularity
- Data structures
- Usage of advanced performance metrics

## [pool_with_closure.py](https://github.com/sam-slate/dsd-phenotype-ranking-example-code/blob/master/pool_with_closure.py)
### Purpose:
A script that runs another multiprocessing script defined by a function and closure template on a given set of input using python's multiprocessing library
### Lower Level description:
A script that runs a higher order function based on a template imported from another file. It runs this function on a given folder of data using the map function from python's pool processing library. It also imports a closure from the other file to use in the mapping function. There are three basic functionalities:
- **Read input folders:**
  - Retrieves input folders and prepares them for mapping
- **Run serial processing:**
  - Checks to see if user wishes to run serial processing, and if so, sets up and runs basic serial processing 
  - Uses a python map function on the imported function, prepared input folders, and the imported closure
  - Calculates the time taken to run serial processing
- **Run pool processing:**
  - Prepares arguments for pool mapping
  - Sets the number of cores used in the pool processing
  - Uses the python pool processing map function on the imported function, prepared input folders, and the imported closure
  - Closes and joins the pool, and calculates the time taken to run pool processing

### Concepts used:
- Multiprocessing
- Object oriented programming
- Higher order functions and closures

## [mp_combine.py](https://github.com/sam-slate/dsd-phenotype-ranking-example-code/blob/master/mp_combine.py)
### Purpose: 
A script based on the multi-processing template that combines two rankings to produce a third based on given biases and combination methods
### Lower level description:
Implements a higher order function to be passed into a pool mapping function running on individual rankings. The function takes two rankings and weights them by multiplying each by a set weight. It then combines the two ranks using either addition or multiplcation (chosen by user) and creates a new rank, breaking ties with one of the two original rankings (also as chosen by user). 

### Concepts used:
- Object oriented programming
- Higher order functions 
- Data manipulation

# File structure

Our file structure for storing leave-one-out cross validation data. Every protein associated with a phenotype has a collection of seed, test, and ranking files in which the protein is in the test file, the other proteins associated with the phenotype are in the seed file, and the outputted ranking from an algorithm is in the ranking file. All of our scripts run on top of this file structure.

<img src="https://github.com/sam-slate/dsd-phenotype-ranking-example-code/blob/master/file_structure.png?raw=true" alt="File Structure" style="width:304px">
