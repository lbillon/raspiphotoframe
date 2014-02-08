class Image(object):
    def __init__(self, name):
        self.name = name
        self.library = None
        self.surface = None
        self.timestamp = None
        self.full_path = ''

    def __str__(self):
        return self.name

    def get_full_path(self):
        return "{}/{}".format(self.library.root, self.name)
