# Pedigree-generator
Authors: Bernice Chavez Rojas and Shalom J
## General Info:
This program uses NetworkX, a Python packages that helps create, manipulate and analyze complex graphs and networks. A recursive function is used to add generation to a family pedigree. 

## Input:
CSV file containing years (1850-2000) and number of children. The first row of the data set contains the years, while the columns under each year contain the number of children per family. The file toyIPUMS.csv is a smaller example of the larger data set.

## Output: 
A graph containing all of the family members in a multigenerational family will be visualized. 
Additionally, a text file that contains the edge list data will be created with the following line of code:  
```
nx.write_edgelist(graph, f"{user_args.output_prefix}.nx")
```
The edge list text file will contain the parent - child relationship in the following format:  
```
1 3 {}
1 25 {}
```
fam_2kids.nx is a sample edge list file 


The csv data file is composed of data obtained from IPUMS (Integrated Public Use Microdata Series). IPUMS is a database that provides Census and American Community Survey household composition data. 
The CSV file is based on the number of kids per family found between the years 1850 - 2000. 
	
## Recursive Function:  
The goal is to simulate multigenerational families using data from IPUMS CSV file.

Function takes graph, parent, current generation (curGen) and final generation (finalGD) as arguments. The graph is a NetworkX MultiDiGraph (a directed graph that is able to store multi-edges), the directionality of the graph prevents the possibility of a child becoming a parent to their own parent(s) as generations are added. 

Recursion is used to add a new generation to the family by increasing curGen by 1. 

Edge list information is saved as a text file that can later be used in the SLiMulation pipeline.

## Example on how to run code 
```
python GS_Creating_Families_SG_2.py -y 1880 1900 1920 -c toyIPUMS.csv -o Family.nx
```

## Informative way to run code
```
python GS_Creating_Families_SG_2.py -y year1 year2...yearn -c toyIPUMS.csv -o Filename.nx 
```
'''This line of code run the program'''
