"""
'helpers.py' is created by 'invaana' for the project 'chatbot-ai-engine' on 14 December, 2016. 

"""

__author__ = 'rrmerugu'


import logging, os, time
logger = logging.getLogger(__name__)


def getElapsedTime(t ):
    return '%.2fs'%(float(time.time() - t))



ScrapeHTMLErrorMesg = "Unable to scrape the content"
