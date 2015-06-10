Python daemon template
======================

This script creates a python daemon project with all stuff usually required for server applications 
so you can focus on the code your daemon is supposed to run

The script prepares....

 - forking to background
 - writing/deleting the PID file
 - set up logging to syslog
 - program argument handling
 - template code for config file handling
 - python packaging config (setup.py)
 - linux distribution init/systemd scripts
 

How-To
------

 - check out this project from github
 - run the makeapplication.py script with your project information to create the daemon project
 
Example:
```
./makeapplication.py -d ~/workspace/DemoDaemon/ \
 --short-name guybrush \
 --long-name "guybrush's insult sword fighting daemon" \
 --executable-name insultfight \
 --short-description="automatically starts insult sword fighting battles" \
 --long-description="guybrush automatically attacks everyone with nasty insults like 'you fight like a cow'" \
 --author-name="Guybrush Threepwood" \
 --author-email="threepwood@monkeyisland.example.com" \
 --website="http://www.insultswordfighting.example.com/"
```

 - search the generated code for "TODO: " comments and add your code
 - python setup.py install
 - copy the appropriate init script/service file for your distribution from extra/distributionscripts to /etc/init.d  or /usr/lib/systemd/system
 - service <shortname> start / systemctl start <shortname>
 

