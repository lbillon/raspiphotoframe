import pickle
import random
import threading

__author__ = "lbillon"
__date__ = "$Jan 29, 2014 11:44:13 AM$"

import pygame
import logging


class Loader(threading.Thread):
    def __init__(self, config, q):
        self.__queue = q
        self.__config = config
        self.__image_list = []
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self._load_library_file()


    def run(self):
        images = []
        logging.debug('Loader started')
        done = False
        while not done:
            image = self._pick_image()
            path = image.get_full_path()

            img = pygame.image.load(path)
            (w, h) = img.get_size()
            ratio = w / float(h)
            nw = int(ratio * 1080)
            img = pygame.transform.scale(img, (nw, 1080))

            surface = pygame.Surface((1920, 1080))
            surface.blit(img, (0, 0))
            image.surface = surface
            self.__queue.put(image)
            logging.debug('Loader added surface')


    def _load_library_file(self):
        self.__image_library = pickle.load(open(self.__config['img_file_path'], "rb"))
        self.__image_list = [image for lib in self.__image_library for image in lib.images]
        print(self.__image_list)


    def _pick_image(self):
        if not self.__image_list:
            self._load_library_file()

        image = random.choice(self.__image_list)
        self.__image_list.remove(image)

        return image

