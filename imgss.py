from queue import *
import sys
import os
import logging
from imgss.config import Config
from imgss.loader import Loader
from imgss.slideshow import Slideshow


def scan_images(config):
    logging.info('Scanning')    
    folder = sys.argv[2]
    try:
        os.remove(config['img_file_path'])
    except OSError:
        pass
    
    for root, dirs, files in os.walk(folder):
        gen = (i for i in files if i.endswith('.jpg'))
        for x in gen:
            path = root+'/'+x
            with open(config['img_file_path'], "a") as myfile:
                myfile.write(path+'\n')            

def slideshow(config):

    ss = Slideshow(q)
    ss.run()
    loader_object = Loader()
    loader_object.run()



q = Queue(10)
config = Config()
logging.basicConfig(filename='img.log',level=logging.DEBUG)
logging.info('Started')

try:
    scan=('-s' == sys.argv[1])
except IndexError:
    scan=False

if scan:
    scan_images(config)
else:
    slideshow(config)
        
        
    



