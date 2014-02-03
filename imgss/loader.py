import random
import threading
import sys

__author__ = "lbillon"
__date__ = "$Jan 29, 2014 11:44:13 AM$"

import pygame
import logging


class Loader(threading.Thread):
    def __init__(self, config, q):
        self.__queue = q
        self.__config=config
        threading.Thread.__init__(self)
        self.setDaemon(True)


    def run(self):
        lines = []
        logging.info('Loader started')
        done = False
        while not done:
            if 0 == len(lines):
                lines = open(self.__config['img_file_path']).read().splitlines()
            path = random.choice(lines)
            lines.remove(path)

            img = pygame.image.load(path)

            (w, h) = img.get_size()
            ratio = w / float(h)
            nw = int(ratio * 1080)
            img = pygame.transform.scale(img, (nw, 1080))

            surface = pygame.Surface((1920, 1080))
            surface.blit(img, (0, 0))
            self.__queue.put(surface)
            logging.info('Loader added surface')