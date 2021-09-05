import sys
import os
from scrapy.cmdline import execute #Import and execute scrapy command method

sys.path.append (os.path.join (os.getcwd())) #Add a new path to the Python interpreter, add the directory where the main.py file is located to the Python interpreter
execute (['scrapy', 'crawl', 'IITD','--nolog']) #execute the scrapy command

