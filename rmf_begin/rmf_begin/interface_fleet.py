from array import array
import pygame as pg
import yaml
from tkinter import *
from tkinter import filedialog
import networkx as nx
from networkx import DiGraph
import matplotlib.pyplot as plt
import numpy as np
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from numpy import array


class Begin():
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.screen = pg.display.set_mode((self.width,self.height))
        pg.display.set_caption('gui')

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
        print('Write Done !')
    
    def read_matrix(self,filename):
        print('Reading file . . .')
        fname = filename
        with open(fname,"r") as f:
            loaded = yaml.safe_load(f)
        self.A_matrix = loaded.get('Adjacency Matrix')
        loaded = np.array(loaded)
        # print(loaded)
        print('Read Done !')
        
        return loaded


class Draw():
    def __init__(self):  
        self.update = pg.display.update()
        self.flag_draw = 0
    def circle(self,pos_x,pos_y,radius):
        pg.draw.circle(begin.screen, (0, 255, 0),[pos_x, pos_y],radius)
        self.update
    def line(self,x1,y1,x2,y2):
        pg.draw.line(begin.screen, (255, 0, 0), (x1, y1), (x2, y2))
        self.flag_draw =1
        pg.display.flip()
    
    def show_nx_graph(self):
        pos = nx.get_node_attributes(G,'pos')
        labels = nx.get_edge_attributes(G,'weight')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
        nx.draw(G,pos,with_labels = True,arrows = True)
        plt.show()
        

class NX():
    def __init__(self):
        self.pickup_node =[]
        self.depot_node =[]
        self.dropoff_node =[]
        self.nodelist=[]
        self.astar_path = 0
        self.astar_path_cost=[]
        self.adjMatrix=[]
        self.isPathAavailable=0
        self.demand_list=dict

    def astar(self,start_node,end_node):
        self.astar_path = nx.astar_path(G,str(start_node),str(end_node), heuristic = None ,weight='weight')
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
                    path = self.astar(i,j)             
                except :
                    flag = 2
                if(flag == 0):
                    path = self.astar(i,j)
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
        # print(path)
        # print(sum)                  
        # print(self.adjMatrix)
        return self.adjMatrix
                
               




if __name__ == '__main__':
    pg.init()
    pg.font.init()
    begin = Begin()
    draw = Draw()
    nw = NX()
    G = DiGraph()
    num_pressadd = 0
    screen_list=[]
    select_file = Select_file()
    state=0
    bg = pg.image.load(select_file.image_file)
    bg = pg.transform.scale(bg, (begin.width, begin.height))
    rect = bg.get_rect()
    screen = begin.screen
    screen.fill((255,255,255))
    rect = rect.move((0, 0))

    while (1):
        if state==0:
            screen.blit(bg,rect)
            pg.display.update()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    exit()
            state=1
        
        elif state==1:
            mouse = pg.mouse.get_pos() 
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                elif event.type == pg.MOUSEBUTTONDOWN and event.button==1:
                    current_screen = pg.Surface.copy(begin.screen)
                    screen_list.append(current_screen)
                    draw.circle(mouse[0],mouse[1],begin.width//100)
                    num_pressadd+=1
                    
                elif event.type == pg.MOUSEBUTTONDOWN and event.button==3:
                    if num_pressadd>=0:
                        num_pressadd = num_pressadd-1
                        begin.screen.blit(current_screen,(0,0))
            pg.display.update()
            state=2

        elif state==2:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            for n,p in select_file.node_list_yaml.items():
                G.add_node(n,pos=p)
                nw.nodelist.append(n)
            for s,e in select_file.edge_list_yaml.items():
                G.add_edge(str(e[0]),str(e[1]),weight = e[2])
                nw.astar_path_cost.append(e[2])
            for c,v in select_file.assign_node.items():
                if c == "pick_up":
                    nw.pickup_node+=v
                if c == "depot":
                    nw.depot_node+=v
                if c == "drop off":
                    nw.dropoff_node+=v

            #DEMAND node : amount
            nw.demand_list = select_file.demand_node_yaml

            #Sum a* path cost 
            adj_matrix = nw.adjacency_matrix(nw.nodelist) 

            # Write file
            # select_file.write_file({"Adjacency Matrix": np.matrix.tolist(adj_matrix)},'QQQ.yaml')  
        
            # Read file
            select_file.read_matrix('QQQ.yaml')

            state =3


        elif state==3:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            
           

           
            if select_file.timeread==0:
                A = select_file.A_matrix
                A = np.array(A)
                A = array(A,dtype=[("cost", int)])
                B = from_numpy_matrix(A, create_using=nx.DiGraph())
                set_node_attributes(B, values=nw.demand_list, name="demand")
                B = relabel_nodes(B, {0: "Source", 10: "Sink"})

                select_file.timeread = 1

            draw.show_nx_graph()
   

            
        
      
                 

            
        
        