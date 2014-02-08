__author__ = 'lbillon'

import unittest
from raspiphotoframe.config import Config


class MyTestCase(unittest.TestCase):
    def test_init(self):
        c = Config()
        print (c['seconds_per_image'])
        print (c['img_file_path'])



if __name__ == '__main__':
    unittest.main()
