import ConfigParser

class Config(object):
    """This class parses the ini file """
    parser = ConfigParser.RawConfigParser()

    def __init__(self, iniFilePath):
        self.parser.read(iniFilePath)
        pass

    def __get_config__(self,section, option):
        return self.parser.get(section, option)

    def __get_int_config__(self, section, option):
        return self.parser.getint(section, option)
        

    def __get_float_config__(self, section, option):
        return self.parser.getfloat(section, option)


