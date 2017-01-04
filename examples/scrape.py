import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCIDER_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCIDER_PATH)




from scout.scider.tasks import scrape_website_task
from scout.scider import helpers
from scout.db.mongo import connect
connect('scout')

config_file = "configs/github.json"
config = helpers.read_json_file(config_file)

print scrape_website_task(config=config, max_limit=3000, save=True)
#print data["status"]
