class Image(object):
    def __init__(self, name):
        self.name = name
        self.library_name = ''
        self.surface = ''
        self.library = None
        self.timestamp = ''

    def __str__(self):
        return self.name

    def get_full_path(self):
        return "{}/{}".format(self.library.root, self.name)