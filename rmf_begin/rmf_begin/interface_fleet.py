from array import array
from fileinput import filename
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
from vrpy import VehicleRoutingProblem
from PIL import Image

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
        plt.ioff()

    def sourcesink_nx_graph(self):
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos, edge_color='r', arrows = True)
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
        self.prob = 0
        self.route = []
        self.route_astar = []

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
    pg.init()
    pg.font.init()
    begin = Begin()
    draw = Draw()
    nw = NX()
    G = DiGraph()
    num_pressadd = 0
    time_run=1
    screen_list=[]
    select_file = Select_file()
    state=0
    bg = pg.image.load(select_file.image_file)    # load image from yaml to overlay on pygame
    bg = pg.transform.scale(bg, (begin.width, begin.height))
    rect = bg.get_rect()
    screen = begin.screen
    screen.fill((255,255,255))
    rect = rect.move((0, 0))
    t =[]
    t1=[]
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
                elif event.type == pg.MOUSEBUTTONDOWN and event.button==1: #if left click ,Add node at mouse pos
                    current_screen = pg.Surface.copy(begin.screen)
                    screen_list.append(current_screen)
                    draw.circle(mouse[0],mouse[1],begin.width//100)
                    num_pressadd+=1
                    
                elif event.type == pg.MOUSEBUTTONDOWN and event.button==3:  #if right click ,Undo one time
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
            for n,p in select_file.node_list_yaml.items():  #Add nodes from yaml
                G.add_node(str(n),pos=p)
                nw.nodelist.append(n)
            for s,e in select_file.edge_list_yaml.items():  #Add edge from yaml
                G.add_edge(str(e[0]),str(e[1]),weight = e[2])
                nw.astar_path_cost.append(e[2])

            # for c,v in select_file.assign_node.items():     #Assign nodes from yaml
            #     if c == "pick_up":
            #         nw.pickup_node+=v
            #     if c == "depot":
            #         nw.depot_node+=v
            #     if c == "drop off":
            #         nw.dropoff_node+=v
      

            #Sum a* path cost to matrix
            adj_matrix = nw.adjacency_matrix(nw.nodelist) 
            

            # Write file (set variable timerun=0)
            if time_run==0:
                select_file.write_file({"Adjacency Matrix": np.matrix.tolist(adj_matrix)},'QQQ.yaml')  
                time_run=1
        
            # Read file (set variable timerun=1)
            select_file.read_matrix('QQQ.yaml')

            #get pickup,delivery,amount
            nw.demand_list = select_file.demand_node_yaml
            
            state =3


        elif state==3:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            #save G graph as G-backup
            G_backup = G

            # Do only 1 time
            if select_file.timeread==0:
                draw.show_nx_graph()
                A = array(select_file.A_matrix,dtype=[("cost", float)])
                G = from_numpy_matrix(A, create_using=nx.DiGraph())
                last_node = nw.nodelist[-1]
                #plt.savefig(fname='Graph')
                #plt.show()
                

                G = relabel_nodes(G, {0: "Source", last_node: "Sink"})  #set 0 as Source and lastnode as Sink
                for u,v in nw.demand_list.items():
                    G.nodes[v[0]]["request"] = v[1]
                    G.nodes[v[0]]["demand"] = v[2]
                    G.nodes[v[1]]["demand"] = -v[2]
                nw.prob = VehicleRoutingProblem(G,load_capacity=5,num_stops=5,pickup_delivery=True)
                nw.prob.solve(cspy=False)

                best_route = nw.prob.best_routes
                
                print("Best Routes  = ",nw.prob.best_routes)
                #print("Best Values  = ",nw.prob.best_value)


                for s,e in best_route.items():
                    t.append(e)
                for i in range(0,len(t)):
                    nw.route=[]
                    t1=[]
                    len_route = len(t[i])
                    for j in range(len_route):
                        if t[i][j] == 'Source':
                            t[i][j] = 0
                        if t[i][j] == 'Sink':
                            t[i][j] = last_node

                    for k in range(len_route-1):
                        t1+=(nw.astar(G_backup,t[i][k],t[i][k+1]))
                    t1[0]='Source'
                    t1[-1]='Sink'
                    nw.route = list(dict.fromkeys(t1))
                    nw.route_astar.append(nw.route)          
                print(nw.route_astar)    
                select_file.timeread = 1

            # draw.show_nx_graph()
   

            
        
      
                 

            
        
        