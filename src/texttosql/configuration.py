import configparser

class Config:
    def __init__(self, config_file:str):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get(self, section:str, key:str):
        return self.config.get(section, key)
    