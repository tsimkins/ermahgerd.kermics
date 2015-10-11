#!/home/simkintr/python/projects/ermahgerd.kermics/python

activate_this = '/home/simkintr/python/projects/ermahgerd.kermics/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/home/simkintr/python/projects/ermahgerd.kermics/app')

from kermics import app as application
