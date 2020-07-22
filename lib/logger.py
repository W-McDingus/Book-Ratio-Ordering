import os
import sys
import logging
from datetime import datetime

def __expandargs(*s):
    return ''.join(['{0}'.format(t) for t in s])

def LOG(*s):
    pstr = __expandargs(*s)
    logger = logging.getLogger()
    d = {'type':' '}
    logging.warning('%s', pstr, extra=d)

def LOGE(*s):
    pstr = __expandargs(*s)
    logger = logging.getLogger()
    d = {'type':'e'}
    logging.warning('%s', pstr, extra=d)

def LOGINIT(appname):
    now = datetime.now()
    datedir = now.strftime("%Y_%m_%d")
    logdir = os.path.join(os.path.expanduser('~'), 'log')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    datedir = os.path.join(os.path.expanduser('~'), 'log', datedir)
    if not os.path.exists(datedir):
        os.mkdir(datedir)
    logfile = datedir + '/' + appname + '_' + now.strftime("%H_%M_%S")
    if os.path.exists(logfile + '.log'):
        logfile = logfile + '_1'
    logfile = logfile + '.log'
    logging.basicConfig(filename=logfile, filemode='w',
            format='%(type)s %(asctime)-15s %(message)s',
            datefmt='%Y_%m_%d:%H:%M:%S')
    LOG('LOGINIT: ', logfile)

