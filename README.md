Python daemon template
======================

This script creates a python daemon project with all stuff usually required for server applications 
so you can focus on the code your daemon is supposed to run

The script prepares....

 - forking to background
 - write PID file
 - set up logging to syslog
 - template code for config file handling
 - python packaging config (setup.py)
 - init/systemd scripts
 

How-To
------

 - check out this project from github

 - run the makeapplication.py script with your project information  
 

```
./makeapplication.py -d ~/workspace/DemoDaemon/ \
 --short-name guybrush \
 --long-name "guybrush's insult sword fighting daemon" \
 --short-description="automatically starts insult sword fighting battles" \
 --long-description="guybrush automatically attacks everyone with nasty insults like 'you fight like a cow'" \
 --author-name="Guybrush Threepwood" \
 --author-email="threepwood@monkeyisland.example.com" \
 --website="http://www.insultswordfighting.example.com/"
```
