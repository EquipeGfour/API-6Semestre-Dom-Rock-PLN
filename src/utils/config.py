from configparser import ConfigParser
from os import getcwd



DEFAULT_FILE_NAME= "config.ini"

class Config():
    def __init__(self, file_name=DEFAULT_FILE_NAME):
        self._file = file_name
        self._g = self._init_config_parser()


    @property
    def g(self):
        return self._g


    def _init_config_parser(self) -> ConfigParser:
        path = getcwd().replace("src","") + "\\" + self._file
        config = ConfigParser()
        config.read(path)
        return config
