from raspiphotoframe.image import Image


class ImageLibrary(object):
    def __init__(self, root, name):
        self.root = root
        self.name = name
        self.images = []

    def add_image(self, image:Image):
        self.images.append(image)
        image.library = self

    def __str__(self):
        return self.name
