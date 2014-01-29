# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="lbillon"
__date__ ="$Jan 29, 2014 11:02:24 AM$"

import threading

class ImageLoader(threading.Thread):
    def __init__(self, url):
        self.url = url
        self.result = None
        threading.Thread.__init__(self)
        
        
    def run(self):
        lines =[]
        logging.info('Loader started')   
        done=False
        while not done:
            if(0==len(lines)):
                    lines = open(sys.argv[1]).read().splitlines()
            path =random.choice(lines)
            lines.remove(path)

            img=pygame.image.load(path) 
            (w,h)=img.get_size()
            ratio=w/float(h)
            nw=int(ratio*1080)
            img=pygame.transform.scale(img, (nw, 1080))

            surface = pygame.Surface(screen.get_size())
            surface.blit(img,((1920-nw)/2,0))
            myfont = pygame.font.SysFont("freesans", 30)
            label = myfont.render(str(len(lines)), 1, (255,255,255))
            surface.blit(label, (0, 0))
            q.put(surface)
            logging.info('Loader added surface')