import pickle
import random
import threading
import logging
import time

import pygame
import exifread

from imgss.image import Image


class Loader(threading.Thread):

    def run(self):
        images = []
        logging.debug('Loader started')
        done = False
        while not done:
            image = self._pick_image()

            self._extract_metadata(image)
            img = pygame.image.load(image.full_path)
            (w, h) = img.get_size()
            ratio = w / float(h)
            nw = int(ratio * 1080)
            img = pygame.transform.scale(img, (nw, 1080))

            surface = pygame.Surface((1920, 1080))
            surface.blit(img, (0, 0))
            image.surface = surface
            self._queue.put(image)
            logging.debug('Loader added surface')

    def __init__(self, config, q):
        self._queue = q
        self._config = config
        self._image_list = []
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self._load_library_file()

    def _load_library_file(self):
        self._image_library = pickle.load(
            open(self._config['img_file_path'], "rb"))
        self._image_list = [image for lib in self._image_library for image in
                            lib.images]

    def _pick_image(self):
        if not self._image_list:
            self._load_library_file()

        image = random.choice(self._image_list)
        self._image_list.remove(image)

        return image

    def _extract_metadata(self, image:Image):
        file = open(image.full_path, 'rb')
        tags = exifread.process_file(file, details=False,
                                     stop_tag='EXIF DateTimeOriginal')
        try:
            image.timestamp = time.strptime(str(tags['EXIF DateTimeOriginal']),
                                            "%Y:%m:%d %H:%M:%S")
        except:
            image.timestamp = 0
            raise




