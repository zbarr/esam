#!/usr/bin/python

__author__ = 'hatim basir'
import sys
import os
import logging
import logging.handlers

class LogBase(object):
    log_levels = {
            1 : logging.DEBUG,
            2 : logging.INFO,
            3 : logging.WARN,
            4 : logging.ERROR,
            5 : logging.CRITICAL,
    }

    def __init__(self, name=None, stream=False, level=2, formatter=None):
        if level in range(1, 5):
            level = self.log_levels.get(level)

        logpath = os.path.dirname(sys.argv[0])
        if name:
            # name = sys._getframe(1).f_globals.get('__file__')
            log_name = name
        else:
            log_name = os.path.basename(sys.argv[0])
            # log_name = os.path.join(os.path.realpath(os.path.dirname(sys._getframe(1).f_globals.get('__file__'))), name)

        self.full_log_name = os.path.join(logpath, log_name) + '.log'
        self.logger = logging.getLogger(log_name)
        if formatter:
            self.formatter = formatter
        else:
            self.formatter = logging.Formatter('%(asctime)s - %(lineno)s - %(module)s - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.logger.setLevel(logging.DEBUG)

        if stream:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(self.formatter)
            if not len(self.logger.handlers):
                self.logger.addHandler(ch)
            # print ("added ch")
        elif os.isatty(sys.stdin.fileno()) or not stream:
            fh = logging.handlers.RotatingFileHandler(self.full_log_name, maxBytes=10485760, backupCount=0)
            fh.setLevel(level)
            fh.setFormatter(self.formatter)
            self.logger.addHandler(fh)
            # print ("added log file")
        else:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(self.formatter)
            if not len(self.logger.handlers):
                self.logger.addHandler(ch)
            # print ("added ch")

        self.logger.debug("Setting log level: %d", level)

    def set_log_level(self, level):
        if level in range(1, 5):
            level = self.log_levels.get(level)

        self.logger.setLevel(level)
if __name__ == "__main__":
    # 'application' code
    # lg = LogBase("test", True)
    print (os.isatty(sys.stdin.fileno()))
    lg = LogBase(stream=True, level=1)
    lg.logger.debug('debug 1 message')
    lg.logger.info('info 1 message')
    lg.logger.warn('warn 1 message')
    lg.logger.error('error 1 message')
    lg.logger.critical('critical 1 message')

    lg2 = LogBase(level=3)
    lg2.logger.debug('debug file message')
    lg2.logger.info('info file message')
    lg2.logger.warn('warn file message')
    lg2.logger.error('error file message')
    lg2.logger.critical('critical file message')

    lg3 = LogBase(name='/tmp/name_test', level=logging.INFO)
    lg3.logger.debug('debug name message')
    lg3.logger.info('info name message')
    lg3.logger.warn('warn name message')
    lg3.logger.error('error  name message')
    lg3.logger.critical('critical  name message')