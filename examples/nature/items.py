"""
'items.py' is created by 'invaana' for the project 'scout' on 15 December, 2016. 

"""

import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCIDER_PATH = os.path.join(CURRENT_PATH, '../../') #adding the project to the python path
sys.path.append(SCIDER_PATH)

from scout.scider.tasks import scrape_website_task
from scout.scider import helpers
from bs4 import BeautifulSoup
import requests
import logging



__WEBSITE__ = "http://www.nature.com"

# STEP1 : Get publication links from http://www.nature.com/siteindex/index.html



def get_all_publications(url):
    urls = []
    res  = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")

    for i, box in enumerate(soup.select('ul.a2z-index-list')):
        if i in [0,3]:
            box_soup = BeautifulSoup(box.prettify(), "lxml")
            for link in box_soup.find_all('a'):
                link_href =  link.get('href')
                if "://" not in link_href:
                    link_href = "%s%s"%(__WEBSITE__,link_href)
                urls.append(link_href)
    return urls


publication_urls =  get_all_publications('http://www.nature.com/siteindex/index.html')



print  publication_urls



# STEP2: goto archives and get the links of archives


def get_archives_links(url):
    archive_url = "%s%s?showyears=%s"%(url.rstrip('/'),'/archive/index.html',"-".join(str(x) for x in range(2000,2018)))
    logging.info( archive_url)
    res = requests.get(archive_url)
    soup = BeautifulSoup(res.text,'lxml')
    archive_data_links = []
    for link in soup.select('#content .container a'):
        link_href = link.get('href')
        if "://" not in link_href:
            link_href = "%s%s" % (__WEBSITE__, link_href)
            archive_data_links.append(link_href)

    return  list(set(archive_data_links))



archive_links = get_archives_links(publication_urls[0])

print archive_links

# STEP3: go to each archives and get the links of journals

def get_journals_of_archive(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')
    archive_data_links = []
    for link in soup.findAll('a', href=True, text='Full Text'):
        link_href = link.get('href')
        if "://" not in link_href:
            link_href = "%s%s" % (__WEBSITE__, link_href)
            archive_data_links.append(link_href)

    return  list(set(archive_data_links))





journals_links = get_journals_of_archive(archive_links[0])
print "====-=-=-"
print journals_links

# STEP4: goto each journal and get the needed data

def get_journal_data(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'lxml')


print get_journal_data(journals_links[0])
# # STEP2: Sout each publication and get the details content of every journal inside the publications


# for publication in publication_urls:
#     config_file = "configs/github.json"
#     config = helpers.read_json_file(config_file)
#
#     config['config']['website'] = publication
#     scrape_website_task(config, 10, True)
#
