class Config(object):
    DEBUG = False
    API_HANDLER = '/soap/v1'
    WSDL_PATH = './wsdl/'

class LocalConfig(Config):
    DEBUG = True

class DockerConfig(Config):
    pass
