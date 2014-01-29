# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import subprocess

__author__="lbillon"
__date__ ="$Jan 29, 2014 11:44:13 AM$"

from collections import deque
import pygame
import logging
from time import gmtime, strftime

class Slideshow(object):
    
    clock=pygame.time.Clock()
    DISPLAYEVENT=pygame.USEREVENT + 1
    rq = deque('',10)
    fq = deque('',10)
    screen_on=True

    def __init__(self,q):
        logging.info('Slideshow initialization...')    
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.time.set_timer(self.DISPLAYEVENT, 6000)
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN ) 
        
        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT])
        
        self.random_queue=q


        self.cs = self.random_queue.get(True,2);
        while True:

            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        return False                
                    if event.key == pygame.K_RIGHT:
                        self.next_image()
                    if event.key == pygame.K_LEFT:
                        self.prev_image()
                    if event.key == pygame.K_SPACE:
                        self.toggle_screen()

                elif (event.type == pygame.USEREVENT+1):
                    self.next_image()

            self.screen.blit(self.cs,(0,0))
            tim=strftime("%H:%M")
            font = pygame.font.SysFont("freesans", 50)
            label = font.render(tim, 1, (255,255,255))
            self.screen.blit(label, (1920-label.get_width()-10,1080-label.get_height()-10))
            pygame.display.flip()
            
    def next_image(self):
        logging.info('Waiting for next image') 
        self.rq.appendleft(self.cs)
        try:
            self.cs=self.fq.popleft()
        except:
            self.cs=self.random_queue.get(True,2)
        logging.info('Got next image') 
        
    def prev_image(self):
        try:
            logging.info('Trying for prev image') 
            prev_image=self.rq.popleft()
            self.fq.appendleft(self.cs)
            self.cs=prev_image
            logging.info('Got prev image')  
        except IndexError:
            logging.info('No prev image')

    def toggle_screen(self):
        if(self.screen_on):
            subprocess.call([ "/usr/sbin/vbetool","dpms","off"])
            pygame.time.set_timer(self.DISPLAYEVENT, 0)
        else:
            subprocess.call([ "/usr/sbin/vbetool","dpms","on"])
            pygame.time.set_timer(self.DISPLAYEVENT, 6000)
        self.screen_on= not self.screen_on



    def run(self):
        pass