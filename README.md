# Scout  


This is a data aggregation framework for scouting and aggregating Scientific Data. 


The framework contains 3 modules:

- **scider** - a scientific data spider  
- **sanitizer** - sanitising the aggregated data to use it further for text mining and processing.
- **db** - database module that stored the data into database (Currently supports MongoDB only)

## How to install


```
#Install scout development version, no stable version yet
pip install -e  git+https://github.com/invaana/scout.git#egg=scout

```

```
sudo apt-get install libxml2-dev libxslt1-dev  libxml2-devel libxslt1-devel python-devel gcc \
 libxslt-devel libxml2-devel


```



```bazaar

yum remove postgresql-devel

```
## How to use

### 1. 2step blog data gathering
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



### 3. 3step website as a blog scraping with topics

```
from scout.scider.tasks import scrape_website_task, scrape_website_topics_task
from scout.scider import helpers


CONFIG_FOLDER = 'configs'
config_file = "%s/newscientist.json"%CONFIG_FOLDER
config = helpers.read_json_file(config_file)


# get the topic urls
topics_configs =  scrape_website_topics_task(config=config,
                                             config_folder=CONFIG_FOLDER)['topics_configs']
topics_configs_count = len(topics_configs)
print topics_configs
print "Found %s topics "%topics_configs_count

# gather data from each topic url
for i, each_config_loc in enumerate(topics_configs):
    if i ==0:
        continue
    print "Now detailed scrapping %s/%s topics" %(i+1, topics_configs_count)
    config_file = each_config_loc
    config = helpers.read_json_file(config_file)
    scrape_website_task(config, 10000, True)

```


```
'ENGINE': 'django.db.backends.postgresql_psycopg2',
'NAME': os.environ.get('LUCY_DB_NAME','kevin_datascout'),
'HOST': os.environ.get('LUCY_DB_HOST','localhost'),
'USER':os.environ.get('LUCY_DB_USER','invaana_user'),
'PASSWORD': os.environ.get('LUCY_DB_PASS','welcome')

```


This module is designed by Data Science team for internal usage at Invaana. 
If you are a scientific data enthusiast, we'd love to know more about your interests. 
Let us know [@invaana](http://twitter.com/invaana) !
