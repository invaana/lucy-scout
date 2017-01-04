from __future__ import absolute_import
__author__ = 'rrmerugu'

"""
'tasks.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.

"""

from scout.settings import worker

import logging, urlparse, decimal, random, os, json
from .scraper import ScrapeHTML, ScrapeDataWithBS4
from time import sleep
from scout.sanitizer import clean_html
from .helpers import validate_config
# from .models import ScrapedData
from scout.db.mongo import ScrapedData
logger = logging.getLogger(__name__)
from scout.settings import dry_run_max_limit


def gen_random_decimal(i,d):
    return decimal.Decimal('%d.%d' % (random.randint(0,i),random.randint(0,d)))


__SLEEP_TIME__ = gen_random_decimal(1, 5)  # generate everytime new


def get_website_name(url):
    domain = urlparse.urljoin(url, '/').rstrip('/')
    logger.debug("Gathering domain from url %s as domain %s"%(url, domain))
    return domain

def get_domain_name(url):
    url = get_website_name(url)
    if '://' in url:
        url = url.split('://')[1].rstrip('/')
    logger.debug('generated the domain %s'%url)
    return url




def make_complete_url(link, website):
    if "http://" in link or "https://" in link or '//' in link:
        return link
    else:
        domain = get_website_name(website)
        logger.debug(domain)
        l = "%s/%s"%(domain, link.lstrip('/') )
        logger.debug("url doesnt have domain, so added that - %s" %l )
        return l


@worker.task()
def test_task():
    return "Super Test Successfull"

def gather_the_links(bs4_scrapper, a, data_points, k, website):
    """
    This will scrape the links, from a page,
    
    :param bs4_scrapper: 
    :param a: 
    :param data_points: 
    :param k: 
    :param website: 
    :return: 
    """
    # links = bs4_scrapper.getArray(a.result['data'],
    #                               data_points[k]['selector'],
    #                               data_points[k]['nthElement'],
    #                               data_points[k]['valueType'])

    links = bs4_scrapper.getValuesDict(a.result['data'],
                                     data_points[k]['selector'],
                                       ['href','text'])
    print links


    links_cleaned = []
    for d in links:
        d['href'] = make_complete_url(d['href'], website)
        links_cleaned.append(d)
    print links_cleaned
    exit()
    return links_cleaned



def save_links(links):
    for link in links:
        try:
            obj = ScrapedData(link=link)
            obj.domain=get_domain_name(link)
            obj.save()
            print obj
            logger.info("Saved the entry %s" % link)
        except Exception as e:
            logger.error(e)
            logger.error("Failed to save the entry %s" % link)


def gather_the_links_of_pagination(old_links, old_links_count, bs4_scrapper, html, k , config, save, max_limit=None): #paginaton
    # TODO - heuristics can be improved
    """
    This is a recursive function that scrapes the pagination part :D

    Heuristics applied with __SLEEP_TIME__ to pause the requests for some time , so that
    we wont bump into "TOO MANY requests " error
    :param links:
    :param bs4_scrapper:
    :param html:
    :param k:
    :param config:
    :param max_limit:
    :return:
    """
    data_points = config['config']['dataPoints']
    links =  gather_the_links(bs4_scrapper, html, data_points, k, config['config']['website'])



    new_links_count = old_links_count + len(links)
    # adding the
    links = links + old_links
    logger.info("Found %s links before pagination " %new_links_count)

    ## Look for next and write a recursion
    next_page_selector  = config['config']['dataPoints']['pagination'] ['nextButton']['selector']
    try:
        next_page_selector_contains =  config['config']['dataPoints']['pagination'] ['nextButton']['contains']
    except:
        next_page_selector_contains = None
    logger.debug("------%s"%next_page_selector_contains)

    #Getting the pagination 'next' url
    if next_page_selector_contains is not None:
        logger.debug("Selector data is %s, %s" %(next_page_selector, next_page_selector_contains))
        next_page_link = bs4_scrapper.getNextUrl(html.result['data'], next_page_selector, next_page_selector_contains , 'href')
        logger.debug("Next page link which contains %s is %s" %(next_page_selector_contains,next_page_link))
    else:
        next_page_link = bs4_scrapper.getString(html.result['data'], next_page_selector,0 , 'href')


    logger.debug("Next page link is %s" %next_page_link)
    if next_page_link == None:
        logger.debug("reached no next url, so pushing whatever sofar done to results")
        if save:
            save_links(links)
        return links

    else:

        next_page_link = make_complete_url(next_page_link, config['config']['website'])


        if max_limit is None:
            max_limit = config['config']['dataPoints']['pagination']['scrapeMaxSize']
        else:
            # overriding the config maxsize
            config['config']['dataPoints']['pagination']['scrapeMaxSize'] = max_limit
        if max_limit is None:
            max_limit = dry_run_max_limit


        now_count = len(links)
        # If found the pagination 'next' url
        logger.debug("Currently scraped %s of max limit %s " %(now_count, max_limit))
        if now_count <= max_limit:

            if next_page_link is not None:

                logger.debug("Sleeping for %s seconds to make this call more realistic/not a bot(heuritics)" %__SLEEP_TIME__)
                sleep(__SLEEP_TIME__)

                 # Time in seconds.
                paginated_html = ScrapeHTML(next_page_link, config['config']['method'])

                if paginated_html.result['status'] == 200:
                    paginated_links = gather_the_links(bs4_scrapper, paginated_html, data_points, k, config['config']['website'])
                    links= links + paginated_links

                    # links contains the first scraped links + paginated links. so no need to add new_links_count again
                    new_links_count = old_links_count + len(links)

                    """
                    TODO -
                    insert the links into db as and when they are scraped, we dont want to carry them with every time,
                    need to duplicate 'links' param in gather_the_links_of_pagination() method.

                    remove links variable to save ram (may be) cause we already pushed them to db, but we still need count
                    """
                    if save:
                        save_links(links)

                    #recurse the function to check if new pagination exists
                    return gather_the_links_of_pagination(links,new_links_count, bs4_scrapper, paginated_html, k , config, save, max_limit  )

                else:
                    logger.debug(paginated_html.result)
                    logger.error(paginated_html.result['mesg'])
                    logger.error("Unable to gather the paginated page data ")

                    if save:
                        save_links(links)
                    # this returns the data that is gathered till failing
                    #TODO- make this failure verbose to the user, so that they can change the params
                    return links

            else:
                if save:
                    save_links(links)
                return links # this is where ths function exists
        else:
            if save:
                save_links(links)
            #max limit reached so sent the links
            return links


def scrape_website_topics_task(config=None, config_folder=None):
    """
    This is the extended form of the scrape_website_task().
    This method scrapes the topics from the blog url first, then
     multiple scrapers are created with the topic url as ['config']['website'] url in the  config.
     So that new config files are called  with the  scrape_website_task method.

    :param config: config file in json with the key ['config]['dataPoints]['topicLinks']
    :param config_folder: config folder to which this new configs should be copied
    :return:
    status : 200
    topics_configs: [] # relative path urls
    """

    validate_config(config)
    scraper_name = config['scraperName']
    response = {}
    logger.debug("Checking if the scraper bot[%s] is requesting for scraping topics links "%scraper_name)
    try:
        topics_scrape_data_point =   config['config']['dataPoints']['topicLinks']
    except:
        logger.debug("no scraping topics requested for the scraper: '%s'" %scraper_name)
        response['links'] = []
        response['status'] = 200
        return response
    if type(topics_scrape_data_point) is not dict:
        raise "Halting the program! 'topicLinks' should be a dict type "



    a = ScrapeHTML(config['config']['website'], config['config']['method'])

    bs4_scrapper = ScrapeDataWithBS4()
    raw_links  = bs4_scrapper.getArray(a.result['data'],
                                              topics_scrape_data_point['selector'],
                                              topics_scrape_data_point['nthElement'],
                                              topics_scrape_data_point['valueType'])
    links  = []
    for link in raw_links:
        links.append(make_complete_url(link, config['config']['website']))



    new_config = config.copy()
    """
        step1: delete the config['config']['dataPoints']['topicLinks']
    so that the new one dont go to topic scraping again
    """
    del new_config['config']['dataPoints']['topicLinks']

    # SANITISE THE SCRAPER NAME
    del new_config['scraperName']
    topic_configs = []


    """
    this will save this config into topic configs
    """
    for i,link in enumerate(links):

        # print config['scraperName']
        """
        step2: modify the website url
        """
        new_config['config']['website'] = link
        new_config['scraperName'] = "%s-topic-%s"%(config['scraperName'],i)
        topics_dir = os.path.join(config_folder, "%s-topics"%config['scraperName'])

        if not os.path.exists(topics_dir ):
            os.makedirs(topics_dir)
        topic_config = "%s/%s.json"%(topics_dir,new_config['scraperName'])
        with open(topic_config ,'w') as f:
            json.dump(new_config, f, indent=4,)
            f.close()
        topic_configs.append(topic_config)
    response['status'] = 200
    response['topics_configs'] = topic_configs
    return response


@worker.task()
def scrape_website_task(config=None, max_limit=None , save=True):
    """
    :param config: config file in dict format
    :param max_limit: max number of entry scraping after which, the scraper should halt
    :param save: should the data be saved to db.
    :return:
    """

    validate_config(config)
    response= {}
    logger.debug("config for this scraping task would be %s" %config)
    a = ScrapeHTML(config['config']['website'], config['config']['method'])
    if a.result['status'] == 200:
        step1_time = a.result['elapsed_time']

        # now go to the second step
        data_points = config['config']['dataPoints']  # this is a dict

        #logger.debug(data_points)
        i = "titles"

        bs4_scrapper = ScrapeDataWithBS4()
        logger.debug(bs4_scrapper)

        # now create a dict for results
        result = {}


        # if config['config']['scrapeType'] == "dryrun":
        #     logger.debug(data_points)
        #     for k, v in data_points.iteritems():
        #         logger.debug(k)
        #         logger.debug(v)
        #         if v['valueSize'] == "string":
        #             result[k] = bs4_scrapper.getString(a.result['data'],
        #                                                data_points[k]['selector'],
        #                                                data_points[k]['nthElement'],
        #                                                data_points[k]['valueType'])
        #         elif v['valueSize'] == "array":
        #             result[k] = bs4_scrapper.getArray(a.result['data'],
        #                                               data_points[k]['selector'],
        #                                               data_points[k]['nthElement'],
        #                                               data_points[k]['valueType'])
        #         else:
        #             result[k] = None
        #
        # if config['config']['scrapeType'] == "list":
        #     for k, v in data_points.iteritems():
        #         if v['valueSize'] == "string":
        #             result[k] = bs4_scrapper.getString(a.result['data'],
        #                                                data_points[k]['selector'],
        #                                                data_points[k]['nthElement'],
        #                                                data_points[k]['valueType'])
        #         elif v['valueSize'] == "array":
        #             result[k] = bs4_scrapper.getArray(a.result['data'],
        #                                               data_points[k]['selector'],
        #                                               data_points[k]['nthElement'],
        #                                               data_points[k]['valueType'])
        #         else:
        #             result[k] = None



        ## first get the links
        k = "links"
        links = []
        links_count = 0
        if config['config']['dataPoints']['pagination']['doPagination']  != True:
            #Step1: Gathering the links
            links = gather_the_links(bs4_scrapper,
                                     a,
                                     data_points,
                                     k,
                                     config['config']['website'])


        if config['config']['dataPoints']['pagination']['doPagination']  == True:
            ## First scape the page
            if max_limit:
                kw = {'max_limit': max_limit}
            else:
                kw = {}

            # overriding the max_limit for dryrun type
            if config['config']['scrapeType'] == 'dryrun':
                kw = {'max_limit': dry_run_max_limit}
            links = gather_the_links_of_pagination(links, links_count, bs4_scrapper, a, k , config, save, **kw)



        result[k] = links = list(set(links))
        result['links_count']= len(links)
        logger.debug("Found %s links after pagination " %len(links))
        """
        Lets insert the data of links into the database
        """

        result['full_details'] = {}
        if  config['config']['scrapeType'] == "detailed":
            # if it is detailed type, the scraper will scrape more more info, ie., every datapoint
            #Step2: Gathering the full details

            logger.debug(links)
            if len(links)>=1:
                to_scrape_points = data_points['linkScraper']
                i = 1
                total = len(links)
                for link in links:
                    #print link


                    logger.debug("Scraping the link %s/%s):%s" %(i,total,link))
                    thishtml = ScrapeHTML(link, config['config']['method'])
                    result['full_details'][link] = {}
                    if thishtml.result['status']== 200:
                        thishtml = thishtml.result['data']
                        for k  in to_scrape_points:
                            logger.debug(k)
                            logger.debug(k["name"])
                            if k['valueSize'] == "string":
                                data = bs4_scrapper.getString(thishtml,
                                                              k['selector'],
                                                              k['nthElement'],
                                                              k['valueType'])
                            elif k['valueSize'] == "array":
                                data = bs4_scrapper.getArray(thishtml,
                                                             k['selector'],
                                                             k['nthElement'],
                                                             k['valueType'])
                            else:
                                data = None

                            result['full_details'][link][k["name"]] = data

                    else:
                        pass

                    i = i +1



        if save:
            logger.debug("Requested to Save the scraped Data | Proceeding...")
            for k,v in result['full_details'].iteritems():
                logger.info("Saving the entry %s" %k)
                logger.debug("Saving the data %s" %v)
                ## check if the url is already saved - if saved just update the data
                ## TODO - we can save multiple versions in FUTURE

                obj = ScrapedData.objects.filter(link = k)
                if obj.count() >= 1:
                    #link already exist so update
                    logger.debug("%s already exist in DB, so updating" %k)
                    try:
                        obj = obj.first()
                        obj.title = v['title']
                        obj.html = clean_html(v['content'])
                        # obj.catagories = v['categories']
                        # obj.tags = v['tags']
                        # obj.images = []

                        if v['date']:
                            obj.publised_date_unformated = v['date']
                        obj.domain = get_domain_name(k)
                        obj.save()
                    except Exception as e:
                        logger.error(e)
                        logger.debug("Failed to update the link %s" %k)
                else:
                    logger.debug("%s doesn't exist in DB, so creating entry" %k)
                    try:
                        obj = ScrapedData(link = k)
                        obj.title = v['title']
                        obj.html = clean_html(v['content'])
                        # obj.catagories = v['categories']
                        # obj.tags = v['tags']
                        # obj.images = []
                        if v['date']:
                            obj.publised_date_unformated = v['date']
                        obj.domain = get_domain_name(k)
                        obj.save()
                        logger.debug("Saved the entry %s" %k)
                    except Exception as e:
                        logger.error(e)
                        logger.debug("Failed to save link %s" %k)


        response['result'] = result

        return {'data': response, 'status':200}
    else:
        response = a.result
        return {'data': response, 'status':400}
