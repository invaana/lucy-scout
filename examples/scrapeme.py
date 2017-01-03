"""
'rsquarelabs_com.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.

"""

import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCIDER_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCIDER_PATH)

from scout.scider.tasks import scrape_website_task, scrape_website_topics_task
from scout.scider import helpers



config_file = "configs/githubnew.json"
config = helpers.read_json_file(config_file)



print scrape_website_topics_task(config, None, True)
# scrape_website_task(config, 10, False)
#





"""
from scout.scraper import ScrapeDataWithBS4, ScrapeHTML
d = ScrapeHTML('http://rsquarelabs.com')
with open("%s.log"%__name__,'w') as f:
    f.write(d.result['data'].encode('utf-8'))
print d.result
print "Im done"
"""