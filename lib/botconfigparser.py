import os
import sys
import configparser
sys.dont_write_bytecode = True
sys.path.insert(0, "../lib")
from logger import LOGINIT,LOG,LOGE

class BotConfigParser:

    def __init__(self):
        self.cfg = None
        self.path = (os.getcwd()).replace('bin', 'setup')
        self.filenm = sys.argv[0].split('/')[-1].replace('.py','.cfg')

    def logconfig(self):
        for s in self.cfg.sections():
            LOG('CFG: section: ', s)
            for k,v in self.cfg[s].items():
                LOG('CFG: key:{} val:{}'.format(k,v))

    def overrideflnm(self, flnm):
        self.filenm = flnm

    def overridepath(self, path):
        self.path = path

    def getsection(self, section):
        return self.cfg[section]

    def loadcfg(self):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(self.path + '/' + self.filenm)
        LOG('BotCfg: from path:{} name:{}'.format(self.path, self.filenm))
        self.logconfig()
        return self.cfg

    def loadcfgwithpath(self, pathcfg):
        self.cfg = configparser.ConfigParser()
        self.cfg.read(pathcfg)
        LOG('BotCfg: {}'.format(pathcfg))
        self.logconfig()
        return self.cfg

