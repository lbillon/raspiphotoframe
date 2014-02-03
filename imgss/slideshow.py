# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
import subprocess
import threading

__author__ = "lbillon"
__date__ = "$Jan 29, 2014 11:44:13 AM$"

from collections import deque
import pygame
import logging
from time import strftime
import platform


class Slideshow(threading.Thread):
    def __init__(self, config, q):
        self.__clock = pygame.time.Clock()
        self.__DISPLAYEVENT = pygame.USEREVENT + 1
        self.__rq = deque('', 10)
        self.__fq = deque('', 10)
        self.__screen_on = True

        logging.debug('Slideshow initialization...')
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.time.set_timer(self.__DISPLAYEVENT, int(config['seconds_per_image']) * 1000)
        self.__screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.event.set_allowed(None)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT])

        self.__random_queue = q

        self.current_image = self.__random_queue.get(True, 2)
        threading.Thread.__init__(self)


    def next_image(self):
        logging.debug('Waiting for next image')
        self.__rq.appendleft(self.current_image)
        try:
            self.current_image = self.__fq.popleft()
        except:
            self.current_image = self.__random_queue.get(True, 2)
        logging.debug('Got next image')

    def prev_image(self):
        try:
            logging.debug('Trying for prev image')
            prev_image = self.__rq.popleft()
            self.__fq.appendleft(self.current_image)
            self.current_image = prev_image
            logging.debug('Got prev image')
        except IndexError:
            logging.debug('No prev image')

    def toggle_screen(self):
        if (self.__screen_on):
            self.turn_screen_off()
        else:
            self.turn_screen_on()
        self.__screen_on = not self.__screen_on

    def turn_screen_on(self):
        try:
            if (platform.machine().startswith('arm')):
                pass    #TODO: Doesn't work
            else:
                subprocess.call(["/usr/sbin/vbetool", "dpms", "off"])
            pygame.time.set_timer(self.__DISPLAYEVENT, 6000)
        except:
            logging.error("Unable to turn screen on")

    def turn_screen_off(self):
        try:
            if (platform.machine().startswith('arm')):
                pass    #TODO: Doesn't work
            else:
                subprocess.call(["/usr/sbin/vbetool", "dpms", "off"])
            pygame.time.set_timer(self.__DISPLAYEVENT, 0)
        except:
            logging.error("Unable to turn screen off")


    def run(self):
        while True:
            self.__clock.tick(10)
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

                elif (event.type == pygame.USEREVENT + 1):
                    self.next_image()

            self.__screen.blit(self.current_image.surface, (0, 0))
            tim = strftime("%H:%M")
            font = pygame.font.SysFont("freesans", 50)
            label = font.render(tim, 1, (255, 255, 255))
            self.__screen.blit(label, (1920 - label.get_width() - 10, 1080 - label.get_height() - 10))

            label = font.render(self.current_image.library_name, 1, (255, 255, 255))
            self.__screen.blit(label, (0, 0))

            pygame.display.flip()