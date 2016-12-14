from __future__ import absolute_import
__author__ = 'rrmerugu'

"""
'tasks.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.

"""

from scout.settings import worker

import logging, urlparse, decimal, random
from .scraper import ScrapeHTML, ScrapeDataWithBS4
from time import sleep

# from .models import ScrapedData
from scout.db.mongo import ScrapedData
logger = logging.getLogger(__name__)


def gen_random_decimal(i,d):
    return decimal.Decimal('%d.%d' % (random.randint(0,i),random.randint(0,d)))


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
    links = bs4_scrapper.getArray(a.result['data'], data_points[k]['selector'],
                                                                data_points[k]['nthElement'], data_points[k]['valueType'])

    links_cleaned = []
    for link in links:
        links_cleaned.append(make_complete_url(link, website))
    return links_cleaned

def scrape_single_page(links, bs4_scrapper, html, k , config, max_limit=None): #paginaton
    # TODO - Apply heuristics, so that this wont  bump into "TOO MANY requests " error
    data_points = config['config']['dataPoints']
    links = links +  gather_the_links(bs4_scrapper, html, data_points, k, config['config']['website'])
    logger.debug("Found %s links before pagination " %len(links))

    ## Look for next and write a recursion
    next_page_selector  = config['config']['dataPoints']['pagination'] ['nextButton']['selector']
    next_page_selector_contains =  config['config']['dataPoints']['pagination'] ['nextButton']['contains']

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
        return links
    else:

        next_page_link = make_complete_url(next_page_link, config['config']['website'])


        if max_limit is None:
            max_limit =config['config']['dataPoints']['pagination']['scrapeMaxSize']
        now_count = len(links)
        # If found the pagination 'next' url
        logger.debug("Currently scraped %s of max limit %s " %(now_count, max_limit))
        if now_count <= max_limit:

            if next_page_link is not None:
                __SLEEP_TIME__ = gen_random_decimal(1,5) # generate everytime new
                logger.debug("Sleeping for %s seconds to make this call more realistic/not a bot(heuritics)" %__SLEEP_TIME__)
                sleep(__SLEEP_TIME__)

                 # Time in seconds.
                paginated_html = ScrapeHTML(next_page_link, config['config']['method'])

                if paginated_html.result['status'] == 200:
                    paginated_links = gather_the_links(bs4_scrapper, paginated_html, data_points, k, config['config']['website'])
                    links= links + paginated_links

                    #recurse the function to check if new pagination exists
                    return scrape_single_page(links, bs4_scrapper, paginated_html, k , config, max_limit  )

                else:
                    logger.debug(paginated_html.result)
                    logger.error(paginated_html.result['mesg'])
                    logger.error("Unable to gather the paginated page data ")

                    # this returns the data that is gathered till failing
                    #TODO- make this failure verbose to the user, so that they can change the params
                    return links

            else:
                return links # this is where ths function exists
        else:
            #max limit reached so sent the links
            return links

@worker.task()
def scrape_website_task(config=None, max_limit=None , save=True):
    """
    :param config: config file in dict format
    :param max_limit: max number of entry scraping after which, the scraper should halt
    :param save: should the data be saved to db.
    :return:
    """

    if config is None:
        raise "No config data provided"
    if type(config) is not dict:
        raise "Config file should be dictionary"
    response= {}
    logger.debug("config for this scraping task would be %s" %config)
    a = ScrapeHTML(config['config']['website'], config['config']['method'])
    if a.result['status'] == 200:
        step1_time = a.result['elapsed_time']

        # now go to the second step
        data_points = config['config']['dataPoints']  # this is a dict

        logger.debug(data_points)
        i = "titles"

        bs4_scrapper = ScrapeDataWithBS4()
        logger.debug(bs4_scrapper)

        # now create a dict for results
        result = {}


        if config['config']['scrapeType'] == "list":
            for k, v in data_points.iteritems():
                if v['valueSize'] == "string":
                    result[k] = bs4_scrapper.getString(a.result['data'], data_points[k]['selector'],
                                                            data_points[k]['nthElement'], data_points[k]['valueType'])
                elif v['valueSize'] == "array":
                    result[k] = bs4_scrapper.getArray(a.result['data'], data_points[k]['selector'],
                                                            data_points[k]['nthElement'], data_points[k]['valueType'])
                else:
                    result[k] = None
        elif config['config']['scrapeType'] == "detailed":
            ## first get the links
            k = "links"
            links = []
            if config['config']['dataPoints']['pagination']['doPagination']  != True:
                #Step1: Gathering the links
                links = gather_the_links(bs4_scrapper, a, data_points, k, config['config']['website'])

            if config['config']['dataPoints']['pagination']['doPagination']  == True:
                ## First scape the page
                if max_limit:
                    kw = {'max_limit': max_limit}
                else:
                    kw = {}
                links = scrape_single_page(links, bs4_scrapper, a, k , config, **kw)



            result[k] = links = list(set(links))
            logger.debug("Found %s links after pagination " %len(links))

            #Step2: Gathering the full details
            result['full_details'] = {}
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

                        # for k, v in to_scrape_points.iteritems():
                        #
                        #     if v['valueSize'] == "string":
                        #         data = bs4_scrapper.getString(thishtml, to_scrape_points[k]['selector'],
                        #                                                 to_scrape_points[k]['nthElement'], to_scrape_points[k]['valueType'])
                        #     elif v['valueSize'] == "array":
                        #         data = bs4_scrapper.getArray(thishtml, to_scrape_points[k]['selector'],
                        #                                                 to_scrape_points[k]['nthElement'], to_scrape_points[k]['valueType'])
                        #     else:
                        #         data = None
                        #
                        #     result['full_details'][link][k] = data

                        for k  in to_scrape_points:
                            logger.debug(k)
                            logger.debug(k["name"])
                            if k['valueSize'] == "string":
                                data = bs4_scrapper.getString(thishtml, k['selector'],
                                                                        k['nthElement'], k['valueType'])
                            elif k['valueSize'] == "array":
                                data = bs4_scrapper.getArray(thishtml, k['selector'],
                                                                        k['nthElement'], k['valueType'])
                            else:
                                data = None

                            result['full_details'][link][k["name"]] = data

                    else:
                        pass

                    i = i +1

        if save:
            logger.debug("Requested to Save the scraped Data | Proceeding...")
            for k,v in result['full_details'].iteritems():
                logger.debug("Saving the entry %s" %k)

                ## check if the url is already saved - if saved just update the data
                ## TODO - we can save multiple versions in FUTURE

                obj = ScrapedData.objects.filter(link = k)
                if obj.count() >= 1:
                    #link already exist so update
                    logger.debug("%s already exist in DB, so updating" %k)
                    try:
                        obj = obj.first()
                        obj.title = v['title']
                        obj.html = v['content']
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
                        obj.html = v['content']
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
