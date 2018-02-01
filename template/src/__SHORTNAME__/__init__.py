import logging.config
from .daemon import Daemon

import sys
import time
import signal
import logging
import argparse
import traceback
if sys.version_info[0] == 2:
  import ConfigParser as CP
else:
  import configparser as CP

from logging.handlers import SysLogHandler

class Controller(object):
    def __init__(self,config):
        self.config=config
        self.stay_alive=True
        
        
    def reload(self):
        ##TODO: PUT CODE HERE THAT SHOULD BE EXECUTED ON SIGHUP ##
        ## the new config is set already from the start script
        logging.info("Reloading __SHORTNAME__")
        
    
    def run(self):
        ## TODO: PUT YOUR STARTUP CODE HERE
        # start threads, etc, then run your main loop
        
        ## main loop of the program
        # replace this with your main thread code 
        # or just remove the demo log output after time.sleep if your main code runs in other threads
        while self.stay_alive:    
            try:
                time.sleep(10)
                logging.info("the __SHORTNAME__ daemon says: HELLO WORLD!")
            except KeyboardInterrupt:
                self.stay_alive=False
                
        #main loop exit, call cleanup method
        self._shutdown()
    
    def shutdown(self):
        """Tell the main loop to exit and shut down gracefully"""
        self.stay_alive=False
    
    def _shutdown(self):
        ##TODO: PUT CODE HERE TO SHUT DOWN GRACEFULLY ##
        logging.info("__LONGNAME__ shutting down")
        
    





CONFIGFILE="/etc/__SHORTNAME__/__SHORTNAME__.conf"
CONTROLLER=None

def init_syslog_logging(level=logging.INFO):
    """initialize logging"""
    #logging.basicConfig(level=loglevel)
    logger = logging.getLogger()
    logger.setLevel(level)
    slh=SysLogHandler(address = '/dev/log')
    slh.setFormatter(logging.Formatter("__SHORTNAME__[%(process)d]: %(message)s"))
    #log debug/error messages to syslog info level
    slh.priority_map["DEBUG"]="info"
    slh.priority_map["ERROR"]="info"

    slh.setLevel(level)
    logger.addHandler(slh)
    return logger

def reload_config():
    """reload configuration"""
    ##
    ##TODO: INSERT CODE TO LOAD YOUR CONFIGURATION HERE, eg. :  ##
    #newconfig=CP.ConfigParser()
    #newconfig.readfp(open(CONFIGFILE))

    #dconfdir=os.path.join(os.path.dirname(CONFIGFILE),'conf.d')
    #if os.path.isdir(dconfdir):
    #    filelist=os.listdir(dconfdir)
    #    configfiles=[dconfdir+'/'+c for c in filelist if c.endswith('.conf')]
    #    readfiles=newconfig.read(configfiles)
    #return newconfig

    #we return a dummy dict by default
    return {}


def sighup(signum,frame):
    """handle sighup to reload config"""
    newconfig=reload_config()
    if CONTROLLER!=None:
        CONTROLLER.config=newconfig

    CONTROLLER.reload()

def sigterm(signum,frame):
    CONTROLLER.shutdown()

def main():
    global CONFIGFILE,CONTROLLER

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--foreground",action="store_true",dest="foreground",default=False,help="do not fork to background")
    parser.add_argument("--pidfile",action="store",dest="pidfile")
    parser.add_argument("-c","--config",action="store",dest="config",help="configfile",default="/etc/__SHORTNAME__/__SHORTNAME__.conf")
    parser.add_argument("--log-config",action="store",dest="logconfig",help="logging configuration file")
    parser.add_argument("--user",action="store",dest="user", help="run as user")
    parser.add_argument("--group",action="store",dest="group", help="run as group")
    parser.add_argument("-d","--debug",action="store_true",dest="debug",default=False,help="run in debug mode")

    opts = parser.parse_args()

    #keep a copy of stderr in case something goes wrong
    stderr=sys.stderr
    try:
        daemon=Daemon(opts.pidfile)
        if not opts.foreground:
            daemon.daemonize()
        CONFIGFILE=opts.config
        config=reload_config()

        #drop privileges
        daemon.drop_privileges(opts.user,opts.group)

        if opts.logconfig:
            logging.config.fileConfig(opts.logconfig)

        if opts.foreground:
            if not opts.debug:
                logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')
            else:
                logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
        else:
            #log to syslog
            if not opts.logconfig:
                init_syslog_logging()
            signal.signal(signal.SIGHUP, sighup)
            signal.signal(signal.SIGTERM, sigterm)

        logging.info("__LONGNAME__ starting up...")

        CONTROLLER=Controller(config)
        CONTROLLER.run()

        logging.info("__LONGNAME__ shut down")
    except Exception:
        exc=traceback.format_exc()
        errtext="Unhandled exception in main thread: \n %s \n"%exc
        stderr.write(errtext)
        logging.error(errtext)



