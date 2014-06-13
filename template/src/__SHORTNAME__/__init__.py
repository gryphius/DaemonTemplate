import time
import logging

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
        
    
    