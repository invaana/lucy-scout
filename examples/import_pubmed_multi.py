import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCOUT_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCOUT_PATH)




from scout.pubmed.parse import parse_xml_to_dict, save_dict_to_db
from scout.db import Journal, PublicationKeyword, PublicationType
from django.utils.encoding import smart_str
import gzip, os, time

import ftputil
from multiprocessing import Process
import random
import time

print Journal.objects.all().count()





FILES_PATH = '/home/ec2-user/Downloads/ftp.ncbi.nlm.nih.gov/pubmed/updatefiles'

# FILES_PATH ='/Users/rrmerugu/Projects/invaana/lucy-scout/examples/pubmed'


def gather_data_from_file(fil):
    full_path = "%s/%s" % (FILES_PATH, fil)
    file_content = gzip.open(full_path, 'rb').read()
    thedict = parse_xml_to_dict(file_content=file_content)
    
    total = len(thedict)
    print total
    for i, d in enumerate(thedict):
        try:
            entry = save_dict_to_db(d)
            print "%s/%s - %s" % (i, total, entry)
        except:
            print "Skipped %s/%s" % (i, total)
    os.remove(full_path)
    print "removed %s " % full_path




    print "currently on %s" %fil
    print "pausing for 10 sec for the db operations to relax"
    time.sleep(10)
    gather_data_from_file(fil)
 



processes = []

all_files = os.listdir(FILES_PATH )
for fil in all_files:
    p = Process(target=gather_data_from_file, args=(fil))
    p.start()
    processes.append(p)

for p in processes:
    p.join()


# xmlfile = "pubmed/medsamp2016a.xml"

# # download some files from the login directory
# PUBMED_DIR = '/pubmed/baseline/'
# host = ftputil.FTPHost('ftp.ncbi.nlm.nih.gov', 'anonymous','rrmerugu@gmail.com')
# names = host.listdir(PUBMED_DIR)
# print names
# for name in names:
#     print "Downloading %s "%name
#     print host.path.isfile(name)
#     if host.path.isfile(name):
#         print "Currently downloading %s" %name
#         host.download("%s%s%"%(PUBMED_DIR,name), name, 'b')        # remote, local, binary mode
#         print "Downloading %s done :D" %name
#





