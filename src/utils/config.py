from configparser import ConfigParser

DEFAULT_FILE_NAME= "config.ini"

class Config():
    def __init__(self, file_name=DEFAULT_FILE_NAME):
        self._file = file_name
        self._g = self._init_config_parser()


    @property
    def g(self):
        return self._g


    def _init_config_parser(self) -> ConfigParser:
        config = ConfigParser()
        config.read(self._file)
        return config