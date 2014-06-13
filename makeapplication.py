#!/usr/bin/python
import sys
import optparse
import os
import re

def errout(message):
    sys.stderr.write(message+"\n")

def replace_variables(text,values):
    for k,v in values.iteritems():
        text=text.replace(k,v)
    return text

def transfer(templatedir,targetdir,values,filenameoverrides,permissions):
    if templatedir.endswith('/'):
        templatedir=templatedir[:-1]
        
    for root, dirs, files in os.walk(templatedir):
        
        #strip templatedir
        strippedroot=root[len(templatedir)+1:]
        targetroot=replace_variables(strippedroot,values)
        
        for dirname in dirs:
            targetdirname=replace_variables(dirname,values)
            absolute_targetdir=os.path.abspath(os.path.join(targetdir,targetroot,targetdirname))
            
            print "creating directory: %s"%absolute_targetdir
            if not os.path.exists(absolute_targetdir):
                os.mkdir(absolute_targetdir)
        
        for filename in files:
            if filename in filenameoverrides:
                targetfilename=filenameoverrides[filename]
            else:
                targetfilename=replace_variables(filename,values)
            absolute_targetfile=os.path.abspath(os.path.join(targetdir,targetroot,targetfilename))
            print "writing file: %s"%absolute_targetfile
            
            absolute_sourcefile=os.path.abspath(os.path.join(templatedir,strippedroot,filename))
            source_content=open(absolute_sourcefile).read()
            target_content=replace_variables(source_content,values)
            fp=open(absolute_targetfile,'w')
            fp.write(target_content)
            fp.close()
            
            if os.path.join(strippedroot,filename) in permissions:
                os.chmod(absolute_targetfile, permissions[os.path.join(strippedroot,filename)])
            

if __name__ == '__main__':

    args=sys.argv
    parser=optparse.OptionParser()
    parser.add_option("-d","--directory",action="store",dest="directory",help="target directory for the new project")
    parser.add_option("-n","--short-name",action="store",dest="shortname",help="short name of the project, one word")
    parser.add_option("--long-name",action="store",dest="longname",help="long name of the project, can be multiple words")
    parser.add_option("--short-description",action="store",dest="shortdescription",help="short description of the project")
    parser.add_option("--long-description",action="store",dest="longdescription",help="long description of the project")
    parser.add_option("--author-name",action="store",dest="authorname",help="Author's Name")
    parser.add_option("--author-email",action="store",dest="authoremail",help="Author's Email")
    parser.add_option("--website",action="store",dest="website",help="project website")
    
    (opts,args)=parser.parse_args()
    
    required=['directory','shortname','shortdescription']
    
    for requirement in required:
        if getattr(opts,requirement)==None:
            setattr(opts, requirement, raw_input("%s: "%requirement).strip())
    
    if not re.match('^[a-z]+$',opts.shortname)!=None:
        errout("shortname must be one word with only lowercase letters")
        sys.exit(1)
        
    if opts.longname==None:
        opts.longname=opts.shortname
    if opts.longdescription==None:
        opts.longdescription=opts.shortdescription

    
    values={
        '__SHORTNAME__': opts.shortname,
        '__LONGNAME__': opts.longname,
        '__SHORTDESCRIPTION__': opts.shortdescription,
        '__LONGDESCRIPTION__': opts.longdescription,
        '__AUTHORNAME__': opts.authorname,
        '__AUTHOREMAIL__': opts.authoremail,
        '__WEBSITE__': opts.website,
    }
    
    filenameoverrides={
        '_gitignore':'.gitignore',
    }
    
    permissions={
       'src/bin/__SHORTNAME__':0755,     
       'extra/distributionscripts/centos/6/__SHORTNAME__':0755,          
    }
    
    if not os.path.isdir(opts.directory):
        os.makedirs(opts.directory)
    
    transfer('template',opts.directory,values,filenameoverrides,permissions)

    
