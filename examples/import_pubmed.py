import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCOUT_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCOUT_PATH)




from scout.pubmed.parse import parse_xml_to_dict, save_dict_to_db
from scout.db import Journal, PublicationKeyword, PublicationType
from django.utils.encoding import smart_str
import gzip, os, time

import ftputil
print Journal.objects.all().count()





# FILES_PATH = '/home/ec2-user/pubmed/ftp.ncbi.nlm.nih.gov/pubmed/baseline'
#
FILES_PATH ='/Users/rrmerugu/Projects/invaana/lucy-scout/examples/pubmed'



FILES_PATH = '/home/ec2-user/Downloads/ftp.ncbi.nlm.nih.gov/pubmed/updatefiles'

# FILES_PATH ='/Users/rrmerugu/Projects/invaana/lucy-scout/examples/pubmed'

all_files = os.listdir(FILES_PATH )
print all_files
for fil in all_files:
    print "currently on %s" %fil
    print "pausing for 10 sec for the db operations to relax"
    time.sleep(10)
    if fil.endswith('.xml.gz') or fil.endswith('.xml.gz.back'):
        full_path = "%s/%s" % (FILES_PATH, fil)
        if not os.path.isfile(full_path):
            print "Skipping this ,may be already being run by other scraper "
            continue
        file_content = gzip.open(full_path, 'rb').read()
        new_full_path = "%s.back" %full_path
        if not os.path.isfile(full_path):
            os.rename(full_path, new_full_path)
        else:
            pass