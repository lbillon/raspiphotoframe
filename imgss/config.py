from configparser import ConfigParser


class Config(dict):
    CONFIG_FILE = '/etc/opt/imgss.conf'
    DEFAULTS = {'seconds_per_image': 10, 'img_file_path': '/var/opt/imgss/images.txt'}

    def __init__(self):
        self.__parser = ConfigParser(defaults=self.DEFAULTS)
        self._load_config()
        dict.__init__(self)

    def write_config(self):
        self.__parser.write(self.CONFIG_FILE)

    def _load_config(self):
        parser = self.__parser
        self.__parser.read(self.CONFIG_FILE)

        for k in self.__parser.defaults():
            self[k] = self.__parser.defaults()[k]







