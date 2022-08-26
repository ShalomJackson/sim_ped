import numpy as np
import networkx as nx
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def load_args():
    parser= argparse.ArgumentParser()
    parser.add_argument('-y', '--year_to_sample', nargs='+',type=int)
    parser.add_argument('-c', '--census_filepath', type=str)
    parser.add_argument('-o', '--output_prefix', type=str)
    parser.add_argument('-v', '--verbose', type=bool, default=False)
    parser.add_argument('-p', '--create_plot', type=bool, default=False)
    
    
    return parser.parse_args()


def family(graph, parent1, curGen, finalGenDepth):
    global curPer
    global kids_dict
    
    if(curGen >= finalGenDepth):
        return()
    
    # For current parents, will simulate the number of children they have in this gen 
    kid_num = np.random.choice(kids_dict[years_to_sim[curGen]], size=1)[0] 
    
    parent2 = curPer + 1
    curPer= curPer + 1
    
    if user_args.verbose:
        print("running family: parent1:", parent1, "curPer:", curPer)
        
   
    for i in range(0, kid_num):
            child = curPer + 1
            curPer = curPer + 1
            
            graph.add_edge(parent1, child)  #edge between parent1 and child (curPer)
            
            graph.add_edge(parent2, child)
            
            family(graph, child, curGen + 1, finalGenDepth) #recursion: adds a new generation 
        
            if user_args.verbose:
                
                print("parent1:", parent1, "kid:", child)
                print("parent2:", parent2, "kid:", child)
            
                for sex in range (0, curPer):
                    nx.set_node_attributes(fam_graph, parent1, name='female')
                
    return


if __name__== '__main__':

    user_args = load_args()   
    years_to_sim = user_args.year_to_sample
    census_df = pd.read_csv(user_args.census_filepath)
    
    index = 1
    parent1 = index
    fam_graph = nx.MultiDiGraph()
    cols = []

 # Check to determine if the years imputed are able to be found in the census file
    years_isec = np.intersect1d(census_df.columns.astype(int),years_to_sim)
    
    if len(years_to_sim) != len(years_isec):
        print ('EXIT: Years inputted does not match the years provided in the census file')
        exit (0)
    
  # Sample the number id kids to simulate for each generation
    kids_dict = {} # create a dict where key = generation_year and value = array of #children in generation
    for year in years_to_sim:
        kids_dict[year] = census_df[f'{year}'].to_list()
    
    curPer = 1
    # Call upon recursive function to simulate family pedigree.
    family(fam_graph, parent1, 0, len(years_to_sim))
    
    
    # save edge list 
    nx.write_edgelist(fam_graph, f"{user_args.output_prefix}.nx") #save edge list
    
    # saving attributes 
    #nx.set_node_attributes(family, name="sex" )
    
    if user_args.create_plot:
        nx.draw(fam_graph,with_labels=True, font_weight='bold')
        plt.savefig(f"{user_args.output_prefix}.pdf", format='pdf')
