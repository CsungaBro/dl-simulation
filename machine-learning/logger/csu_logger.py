import logging

class Formatter(logging.Formatter):
    def format(self, record):
        def_format = '%(name)s - %(levelname)s - Message:\n%(message)s'
        if record.levelno == logging.DEBUG:
            self._style._fmt = bcolors.OKBLUE+self.wrapper(def_format,"-")+bcolors.ENDC
        elif record.levelno == logging.INFO:
            self._style._fmt = bcolors.OKGREEN+self.wrapper(def_format,"-")+bcolors.ENDC
        elif record.levelno == logging.ERROR:
            self._style._fmt = bcolors.FAIL+self.wrapper(def_format,"*")+bcolors.ENDC
        else:
          self._style._fmt = "%(levelname)s: %"
        return super().format(record)
    def wrapper(self,mess,sim):
        char_mul = int(100 / len(sim))
        return sim*char_mul+"\n"+ mess+ "\n"+ sim*char_mul

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def logger_init():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger