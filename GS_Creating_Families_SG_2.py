import numpy as np
import networkx as nx
import argparse
import matplotlib.pyplot as plt
import pandas as pd

def load_args():
    parser= argparse.ArgumentParser()
    #parser.add_argument('-v','--verbose')
    parser.add_argument('-y','--year_to_sample', nargs='+',type=int)
    parser.add_argument('-c', '--census_filepath', type=str)
    parser.add_argument('-o', '--output_prefix', type=str)
    
    return parser.parse_args()


def family(graph, parent1, curGen, finalGenDepth):
    global curPer
    
    print(curGen, finalGenDepth)
    if(curGen >= finalGenDepth):
        return()
    
    #print ("running family: parent1:", parent1, "curPer:", curPer)
    #print ("current generation", curGen)
    
    print(num_kids)
    kid = num_kids[curGen] #random number of kids. CHECK HERE
    print("# of kids:", kid)
    
    parent2 = curPer + 1
    curPer= curPer + 1
    #print("parent2/curPer:", curPer)
    
    for i in range(0, kid):
            child = curPer + 1
            curPer = curPer + 1
            
            graph.add_edge(parent1, child)  #edge between parent1 and child (curPer)
            #print ("parent1 + kid:", parent1, child)
            
            graph.add_edge(parent2, child)
            #print ("parent2 + kid:", parent2, child)
            
            family(graph, child, curGen + 1, finalGenDepth) #recursion: adds a new generation
          
    # graph.edges(data=True)
    return

if __name__== '__main__':

    user_args= load_args()   
    years_to_sim= user_args.year_to_sample
    census_df= pd.read_csv(user_args.census_filepath)
    
    index = 1
    parent1 = index
    fam_graph = nx.MultiDiGraph()
    cols=[]

 # Check to determine if the years imputed are able to be found in the census file
    years_isec= np.intersect1d(census_df.columns.astype(int),years_to_sim)
    if len(years_to_sim) != len(years_isec):
        print ('EXIT: Years inputted does not match the tears provided in the census file')
        exit (0)
    
  # Sample the number id kids to simulate for each generation
    num_kids = []
    for year in years_to_sim:
        child_sample= census_df[f'{year}'].sample(n=1).values[0]
        num_kids.append(child_sample)
    print(num_kids)
    
    start_gen = 0
    end_gen = len(years_to_sim)
    
    curPer = 1
    family(fam_graph, parent1, start_gen, end_gen)
    
    nx.write_edgelist(fam_graph, f"{user_args.output_prefix}.nx") #save edge list
    #user_args.verbose
    
    nx.draw(fam_graph,with_labels=True, font_weight='bold')
    plt.savefig(f"{user_args.output_prefix}.pdf", format='pdf')