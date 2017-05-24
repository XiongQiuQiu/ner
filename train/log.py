# -*- coding:utf-8 -*-

import logging

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class logger():

    def __init__(self, name, path, fhlevel = logging.INFO, chlevel = logging.INFO):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        self._path = path
        self.fh_level = fhlevel
        self.ch_level = chlevel

    def filehand(self):
        # 创建一个handler，用于写入日志文件
        self.fh = logging.FileHandler(self._path)
        self.fh.setLevel(self.fh_level)
        self.fh.setFormatter(formatter)
        self._logger.addHandler(self.fh)

    def f_info(self, logmsg):
        self._logger.info(logmsg)

    def f_waring(self, logmsg):
        self._logger.warn(logmsg)

    def f_erroe(self, logmsg):
        self._logger.error(logmsg)

    def f_critical(self, logmsg):
        self._logger.critical(logmsg)

    def streamhandler(self):
        # 再创建一个handler，用于输出到控制台
        self.ch = logging.StreamHandler()
        self.ch.setLevel(self.ch_level)
        self.ch.setFormatter(formatter)
        self._logger.addHandler(self.ch)

    def c_info(self, logmsg):
        self._logger.info(logmsg)

    def c_waring(self, logmsg):
        self._logger.warn(logmsg)

    def c_erroe(self, logmsg):
        self._logger.error(logmsg)

    def c_critical(self, logmsg):
        self._logger.critical(logmsg)

if __name__ == '__main__':
    print 'test'
    logs = logger('test', 'test.log')
    logs.filehand()
    logs.f_info('test')