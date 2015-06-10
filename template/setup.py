from setuptools import setup
import glob


setup(name = "__SHORTNAME__",
    version = "0.0.1",
    description = "__SHORTDESCRIPTION__",
    author = "__AUTHORNAME__",
    url='__WEBSITE__',
    author_email = "__AUTHOREMAIL__",
    package_dir={'':'src'},
    packages = ['__SHORTNAME__',],
    entry_points={
        'console_scripts': [
           '__EXECUTABLE__=__SHORTNAME__:main ',
        ],
    },
    long_description = """__LONGDESCRIPTION__""" ,
    data_files=[
               ('/etc/__SHORTNAME__',glob.glob('conf/*.dist')),
               ('/etc/__SHORTNAME__/conf.d',glob.glob('conf/conf.d/*.dist')),
                ]
) 
