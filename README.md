# Scout  


This is a data aggregation framework for scouting and aggregating Scientific Data. 


The framework contains 3 modules:

- **scider** - a scientific data spider  
- **sanitizer** - sanitising the aggregated data to use it further for text mining and processing.
- **db** - database module that stored the data into database (Currently supports MongoDB only)

## How to install 

```
#Install scout development version, no stable version yet
pip install -e  git+https://github.com/invaana/scout.git@develop#egg=scout

```

## How to use

```
Step1:  Create a scider input json file 
# example : examples/configs/github.json

from scout.scider.tasks import scrape_website_task
from scout.scider import helpers

config_file = "configs/github.json"
config = helpers.read_json_file(config_file)

scrape_website_task(config=config, max_limit=30, save=True) 

:param config: config file in dict format
:param max_limit: max number of entry scraping after which, the scraper should halt
:param save: should the data be saved to db.

```

To run the job in queue `scrape_website_task.delay(config=config, max_limit=30, save=True)`





This module is designed by Data Science team for internal usage at Invaana. 
If you are a scientific data enthusiast, we'd love to know more about your interests. 
Let us know [@invaana](http://twitter.com/invaana) !
