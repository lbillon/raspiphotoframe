# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="lbillon"
__date__ ="$Dec 3, 2013 12:50:36 PM$"


from Queue import *
import pygame
from time import sleep
import sys
import os
import random
import logging
from slideshow import Slideshow
from threading import Thread
from time import gmtime, strftime


def scan_images():
    logging.info('Scanning')    
    folder = sys.argv[2]
    try:
        os.remove('/home/pi/imgs.txt')
    except OSError:
        pass
    
    for root, dirs, files in os.walk(folder):
        gen = (i for i in files if i.endswith('.jpg'))
        for x in gen:
            path = root+'/'+x
            with open('imgs.txt', "a") as myfile:
                myfile.write(path+'\n')            

def slideshow():
    l = Thread(target=loader)
    l.setDaemon(True)
    l.start()
    slideshow = Slideshow(q)

  


def loader():
    lines =[]
    logging.info('Loader started')   
    done=False
    while not done:
        if(0==len(lines)):
                lines = open(sys.argv[1]).read().splitlines()
        path =random.choice(lines)
        lines.remove(path)

        img=pygame.image.load(path)

        (w,h)=img.get_size()
        ratio=w/float(h)
        nw=int(ratio*1080)
        img=pygame.transform.scale(img, (nw, 1080))

        surface = pygame.Surface((1920,1080))
        surface.blit(img,(0,0))
        # myfont = pygame.font.SysFont("freesans", 30)
        # label = myfont.render(str(len(lines)), 1, (255,255,255))
        # surface.blit(label, (0, 0))
        q.put(surface)
        logging.info('Loader added surface')
   
if __name__ == "__main__":
    q = Queue(10)
    
    logging.basicConfig(filename='img.log',level=logging.DEBUG)
    logging.info('Started')    

    try:
        scan=('-s' == sys.argv[1])
    except IndexError:
        scan=False

    if(scan):    
        scan_images()
    else:
        slideshow()
        
        
    



