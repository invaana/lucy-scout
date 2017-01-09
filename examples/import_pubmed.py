import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCOUT_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCOUT_PATH)




from scout.pubmed.parse import parse_xml_to_dict, save_dict_to_db
from scout.db import Journal, PublicationKeyword, PublicationType
from django.utils.encoding import smart_str
import gzip, os

import ftputil
print Journal.objects.all().count()



# xmlfile = "pubmed/medsamp2016a.xml"


FILES_PATH = '/home/ec2-user/pubmed/ftp.ncbi.nlm.nih.gov/pubmed/baseline'

all_files = os.listdir(FILES_PATH )
for fil in all_files:
    print "currently on %s" %fil
    full_path = "%s/%s"%(FILES_PATH,fil)
    f = gzip.open(full_path, 'rb')
    file_content = f.read()
    thedict = parse_xml_to_dict(file_content=file_content)
    total = len(thedict)
    for i, d in enumerate(thedict):
        entry = save_dict_to_db(d)
        print "%s/%s - %s" %(i, total, entry)
    os.remove(full_path)
    print "removed %s "%full_path





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





