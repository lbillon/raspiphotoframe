import pickle
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
        self._load_library_file()



    def run(self):
        images = []
        logging.info('Loader started')
        done = False
        while not done:
            library,image=self._pick_image()
            path = "{}/{}".format(library.root,image.name)

            img = pygame.image.load(path)
            (w, h) = img.get_size()
            ratio = w / float(h)
            nw = int(ratio * 1080)
            img = pygame.transform.scale(img, (nw, 1080))

            surface = pygame.Surface((1920, 1080))
            surface.blit(img, (0, 0))
            image.surface=surface
            self.__queue.put(image)
            logging.info('Loader added surface')



    def _load_library_file(self):
        self.__image_library=pickle.load(open(self.__config['img_file_path'], "rb") )


    def _pick_image(self) :
        library = random.choice([lib for lib in self.__image_library for weight in range(0,len(lib.images))]) #Weighted random choice of library
        image = random.choice(library.images)
        return library,image

