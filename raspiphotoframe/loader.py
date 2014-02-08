import pickle
import random
import threading
import logging
import time

import pygame
import exifread

from raspiphotoframe.image import Image


class Loader(threading.Thread):

    def run(self):
        images = []
        logging.debug('Loader started')
        done = False
        while not done:
            image = self._pick_image()

            self._extract_metadata(image)
            img = pygame.image.load(image.get_full_path())

            (w, h) = img.get_size()

            if (w > h):
                surface = self.create_surface_full_screen(img)
            else:
                surface = self.create_surface_fit(img)

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
        file = open(image.get_full_path(), 'rb')
        tags = exifread.process_file(file, details=False,
                                     stop_tag='EXIF DateTimeOriginal')
        try:
            image.timestamp = time.strptime(str(tags['EXIF DateTimeOriginal']),
                                            "%Y:%m:%d %H:%M:%S")
        except:
            pass

    def create_surface_full_screen(self, image:pygame.image):
        (w, h) = image.get_size()
        ratio = h / float(w)
        nh = int(1920 * ratio)
        offset = (nh - 1080) / 2
        img = pygame.transform.scale(image, (1920, nh))
        surface = pygame.Surface((1920, 1080))
        surface.blit(img, (0, -int(offset)))
        return surface

    def create_surface_fit(self, image:pygame.image):
        (w, h) = image.get_size()
        ratio = w / float(h)
        nw = int(ratio * 1080)
        img = pygame.transform.scale(image, (nw, 1080))
        offset = (1920 - nw) / 2
        surface = pygame.Surface((1920, 1080))
        surface.blit(img, (offset, 0))
        return surface


