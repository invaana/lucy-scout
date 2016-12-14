"""
'scraper.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.



Example usage :

a = ScrapeHTML('http://rsquarelabs.com', 'requests')
print a.result

"""

__author__ = 'rrmerugu'
# -*- coding: utf-8 -*-

import time, requests, urllib2, logging
from bs4 import BeautifulSoup as soup
from . import helpers
from helpers import ScrapeHTMLErrorMesg
logger = logging.getLogger(__name__)


class ScrapeHTML:
    """
    This class is used to scrape the HTML content from url

    Inputs :
    1. url -> string | can be any
    2. scrapingMethod -> string  | [selenium, requests, urllib], default=selenium

    Outputs:
    'status' = 400 | 200 | 500
    'data' = <html><body><h1>Hello World!</h1></body></html>
    'mesg' = Error or Success Message
    'elapsed_time' = time took to scape in seconds

    """

    def __init__(self, url, scrapingMethod="requests"):
        self.t = time.time()
        self.result = self.doTheJob(url, scrapingMethod)

    def getHTMLWithSelenium(self, url):
        # TODO: to be implemented
        return None, None

    def getHTMLWithURLlib(self, url):
        try:
            content = urllib2.urlopen(url, timeout=20).read()
            html = soup(content)
            logger.debug('Loaded page Successfully :' + url)
        except:
            html = None
            logger.debug('Loading page Failed :' + url)
        return html, content

    def getHTMLWithRequests(self, url):
        """
        returns the HTML structure
        """
        response = {}
        try:
            page = requests.get(url, timeout=20)
            dif = helpers.getElapsedTime(self.t)
            if page.status_code == 200:
                response['status'] = 200
                response['data'] = page.text
                response['elapsed_time'] = dif
                response['mesg'] = "Scraped Successfully"
                return response
            else:
                response['status'] = page.status_code
                response['data'] = None
                response['mesg'] = ScrapeHTMLErrorMesg
                response['elapsed_time'] = dif
                return response
        except Exception as e:
            dif = helpers.getElapsedTime(self.t)
            logger.error(e)
            response['status'] = 400
            response['data'] = None
            response['mesg'] = ScrapeHTMLErrorMesg
            response['elapsed_time'] = dif
            return response

    def doTheJob(self, url, sm):
        if sm == "selenium":
            return self.getHTMLWithSelenium(url)
        elif sm == "urllib":
            return self.getHTMLWithURLlib(url)
        elif sm == "requests":
            return self.getHTMLWithRequests(url)
        else:
            return "Invalid method provided for scraping"


class ScrapeWithSelenium:
    pass




class ScrapeDataWithBS4:
    """
    This is the second step part after scraping the HTML -> ie., gathering/scraping the needed data

    Inputs :
    html -> raw html text
    selector -> css/xpath,idw
    num -> nth element
    valueType -> text/innerHTML/src/href

    """

    def getElement(self, html, selector, num):

        try:
            html = soup(html)
            elem = html.select(selector)[num]
        except Exception as e:
            logger.error(e)
            elem = None
        return elem

    def getString(self, html, selector, num, value_type):

        html = html
        css = str(selector)
        value = str(value_type)
        num = int(num)
        # logger.debug("INFO: Gathering the value for [ " + str(css) + " ]["+ str(num)+"]["+str(value)+"]")
        try:
            html = soup(html)
            elem = html.select(css)[num]
            if value == 'text':
                result = elem.get_text().lstrip().rstrip().encode('utf-8')
            elif value == 'innerHTML':
                result = elem.encode('utf-8')
            else:
                result = elem.get(value).lstrip().rstrip().encode('utf-8')

        except Exception as e:
            logger.error(e)
            result = None
        return result

    def getNextUrl(self, html, selector, contains, value_type):
        # TODO - Right now the selector is 0th element, but it can be made to select as nth element which 'contains' some 'selector'
        html = soup(html)
        selector = selector
        contains = contains
        value_type = value_type
        logger.debug("Searching for string %s in selector %s with valuetype %s" % (contains, selector, value_type))
        try:
            import re
            html.find()
            # column = html.find(selector, text=re.compile(contains)) #  , attrs = {'class' : 'pos'}
            if contains is not None:
                column = html.find(selector, text=contains)  # , attrs = {'class' : 'pos'}
            else:
                column = html.find(selector)
            logger.debug(column)
            # logger.debug("Gathering the next url column %s: and %s is %s" %(column, value_type,  column.get(value_type)))
            # logger.debug("Column is %s "%column)

            return column.get(value_type)
        except Exception as e:
            logger.error(e)
            return None

    def getArray(self, html, selector, num, value_type):
        html = html
        css = str(selector)
        value = str(value_type)
        num = int(num)
        # logger.debug("Gathering the array for [ " + css + " ][" + value + "]")
        try:
            html = soup(html)
            elems = html.select(css)
            arr = []
            # logging.debug(str(len(elems)) + " found in the selector'" + css + "'")
            if value == 'text':
                for e in elems:
                    if e.get_text():
                        temp = e.get_text().lstrip().rstrip().encode('utf-8')
                        arr.append(temp)
                        # print temp
            else:
                for e in elems:
                    if e.get(value):
                        temp = e.get(value).lstrip().rstrip().encode('utf-8')
                        arr.append(temp)
                        # print temp
            return arr
        except Exception as e:
            logger.error(e)

            return None


