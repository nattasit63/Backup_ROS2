from array import array
import yaml
from tkinter import *
from tkinter import filedialog
import networkx as nx
from networkx import DiGraph
import matplotlib.pyplot as plt
import numpy as np
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from numpy import array

class Select_file():
    def __init__(self):
        self.root = Tk()
        self.root.filename = filedialog.askopenfilename(initialdir="/home/natta/ros2_ws/src/rmf_begin/yaml",title='Select .yaml file',filetypes=(("yaml file","*.yaml"),("all files","*.*")))
        print("Path to File : ",self.root.filename)
        self.root.destroy()
        with open(self.root.filename,'r') as f:
                yml_dict = yaml.safe_load(f)
        self.image_file = yml_dict.get('drawing')
        self.node_list_yaml = yml_dict.get('node_list')
        self.edge_list_yaml = yml_dict.get('edge_list')
        self.assign_node = yml_dict.get('assign_list')
        self.demand_node_yaml = yml_dict['demand_node']
        self.timeread=0
        self.A_matrix = []
    def write_file(self,data,filename):
            print('Writing to file . . .')
            fname = filename
            with open(fname,"w") as f:
                yaml.dump(data,f)
            print('Done ! (File is write as same path as this python file)')

class NX():
    def __init__(self):
        self.nodelist=[]
        self.astar_path = 0
        self.astar_path_cost=[]
        self.adjMatrix=[]
    def astar(self,graph,start_node,end_node):
        self.astar_path = nx.astar_path(graph,str(start_node),str(end_node), heuristic = None ,weight='weight')
        return self.astar_path

    def adjacency_matrix(self,node_ls):
        sum=0
        size = len(node_ls)
        self.adjMatrix = np.zeros((size,size))
        for i in range(size):
            for j in range(size):
                sum = 0
                flag = 0  
                #0 = Have Path (No Error)
                #1 = Same Point
                #2 = No Path  
                if i==j :
                    flag = 1
                try:
                    path = self.astar(G,i,j)             
                except :
                    flag = 2
                if(flag == 0):
                    path = self.astar(G,i,j)
                    path_size = len(path)
                    for k in range(path_size-1):
                        for s,e in select_file.edge_list_yaml.items():
                            if(int(path[k])==e[0] and int(path[k+1])==e[1]):
                                sum += e[2]
                                break
                    for s,e in select_file.edge_list_yaml.items():
                        if int(i)==int(e[0]):
                            if int(j)==int(e[1]):
                                if(sum != 0):
                                    sum = min(e[2],sum)
                                else:
                                    sum = e[2]
                self.adjMatrix[i][j]= sum             
        return self.adjMatrix

if __name__ == '__main__':
    nw = NX()
    G = DiGraph()
    num_node = 0
    node_pos=[]
    time_run=0
    select_file = Select_file()
    while(1):
        if time_run==0:
            for n,p in select_file.node_list_yaml.items():  #Add nodes from yaml
                G.add_node(str(n),pos=p)
                num_node+=1
                nw.nodelist.append(n)
            for s,e in select_file.edge_list_yaml.items():  #Add edge from yaml
                G.add_edge(str(e[0]),str(e[1]),weight = e[2])
                nw.astar_path_cost.append(e[2])       
            adj_matrix = nw.adjacency_matrix(nw.nodelist) #Sum a* path cost to matrix 
            select_file.write_file({"Adjacency Matrix": np.matrix.tolist(adj_matrix)},'AAAA.yaml')#Write matrix to yaml
            time_run=1
        exit()
        
    