from logging import root
from select import select
import pygame as pg
import yaml
from tkinter import *
from tkinter import filedialog


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
        
if __name__ == '__main__':
    pg.init()
    pg.font.init()
    begin = Begin()
    draw = Draw()
    state = 0
    num_pressadd = 0
    screen_list=[]
    pos_to_draw = [0,0,0,0]
    select_file = Select_file()
    print("Path to File : ",select_file.root.filename)
    select_file.root.destroy()
    with open(select_file.root.filename,'r') as f:
            yml_dict = yaml.safe_load(f)
    image_file = yml_dict.get('drawing')
    bg = pg.image.load(image_file)
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
                    # draw.line(pos_to_draw[0],pos_to_draw[1],120,120)
                    
                elif event.type == pg.MOUSEBUTTONDOWN and event.button==3:
                    if num_pressadd>=0:
                        num_pressadd = num_pressadd-1
                        begin.screen.blit(current_screen,(0,0))

            pg.display.update()


   