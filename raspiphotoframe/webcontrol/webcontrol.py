import threading
import os

import bottle

from raspiphotoframe.slideshow import Slideshow

from raspiphotoframe.config import Config


class WebControl(threading.Thread):
    def run(self):
        templates_dir = os.path.dirname(__file__)
        webapp = _App(self._config, self._slideshow)
        bottle.route("/")(webapp.index)
        bottle.route("/prev")(webapp.prev)
        bottle.route("/next")(webapp.next)
        bottle.TEMPLATE_PATH.append(templates_dir)
        bottle.run(host='0.0.0.0', port=9000)

    def __init__(self, config:Config, slideshow:Slideshow):
        self._config = config
        self._slideshow = slideshow
        threading.Thread.__init__(self)


class _App(object):
    def __init__(self, config:Config, slideshow:Slideshow):
        self._config = config
        self._slideshow = slideshow

    def index(self):
        return bottle.template('index')

    def prev(self):
        self._slideshow.prev_image()
        return bottle.template('index')

    def next(self):
        self._slideshow.next_image()
        return bottle.template('index')




