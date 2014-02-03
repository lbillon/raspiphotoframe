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
    def run(self):
        while self._continue:
            self._clock.tick(10)

            self._handle_events()

            self._screen.blit(self.current_image.surface, (0, 0))

            self._blit_current_time()
            self._blit_image_metadata()

            pygame.display.flip()

    def __init__(self, config, q):
        self._clock = pygame.time.Clock()
        self._DISPLAYEVENT = pygame.USEREVENT + 1
        self._rq = deque('', 10)
        self._fq = deque('', 10)
        self._screen_on = True
        self._continue = True

        logging.debug('Slideshow initialization...')
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.time.set_timer(self._DISPLAYEVENT,
                              int(config['seconds_per_image']) * 1000)
        self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        pygame.event.set_allowed(None)
        pygame.event.set_allowed(
            [pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT])

        self._random_queue = q

        self.current_image = self._random_queue.get(True, 2)
        threading.Thread.__init__(self)

    def _next_image(self):
        logging.debug('Waiting for next image')
        self._rq.appendleft(self.current_image)
        try:
            self.current_image = self._fq.popleft()
        except:
            self.current_image = self._random_queue.get(True, 2)
        logging.debug('Got next image')

    def _prev_image(self):
        try:
            logging.debug('Trying for prev image')
            prev_image = self._rq.popleft()
            self._fq.appendleft(self.current_image)
            self.current_image = prev_image
            logging.debug('Got prev image')
        except IndexError:
            logging.debug('No prev image')

    def _toggle_screen(self):
        if (self._screen_on):
            self._turn_screen_off()
        else:
            self._turn_screen_on()
        self._screen_on = not self._screen_on

    def _turn_screen_on(self):
        try:
            if (platform.machine().startswith('arm')):
                pass    # TODO: Doesn't work
            else:
                subprocess.call(["/usr/sbin/vbetool", "dpms", "off"])
            pygame.time.set_timer(self._DISPLAYEVENT, 6000)
        except:
            logging.error("Unable to turn screen on")

    def _turn_screen_off(self):
        try:
            if (platform.machine().startswith('arm')):
                pass    # TODO: Doesn't work
            else:
                subprocess.call(["/usr/sbin/vbetool", "dpms", "off"])
            pygame.time.set_timer(self._DISPLAYEVENT, 0)
        except:
            logging.error("Unable to turn screen off")

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._continue = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self._continue = False
                if event.key == pygame.K_RIGHT:
                    self._next_image()
                if event.key == pygame.K_LEFT:
                    self._prev_image()
                if event.key == pygame.K_SPACE:
                    self._toggle_screen()

            elif (event.type == pygame.USEREVENT + 1):
                self._next_image()

    def _blit_current_time(self):
        tim = strftime("%H:%M")
        font = pygame.font.SysFont("freesans", 50)
        label = font.render(tim, 1, (255, 255, 255))
        self._screen.blit(label, (
            1920 - label.get_width() - 10, 1080 - label.get_height() - 10))

    def _blit_image_metadata(self):
        font = pygame.font.SysFont("freesans", 30)
        image = self.current_image

        text = image.library.name
        if (image.library.name and image.timestamp):
            text += ", "

        text += strftime("%B %Y", image.timestamp)

        label = font.render(text, 1, (255, 255, 255))
        self._screen.blit(label, (
            1920 - label.get_width() - 10, 0))








