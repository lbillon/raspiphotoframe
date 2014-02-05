class Image(object):
    def __init__(self, name):
        self.name = name
        self.library_name = ''
        self.surface = ''
        self.timestamp = None
        self.full_path = ''

    def __str__(self):
        return self.name
