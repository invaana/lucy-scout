"""
'helpers.py' is created by 'invaana' for the project 'chatbot-ai-engine' on 14 December, 2016. 

"""

__author__ = 'rrmerugu'




import  json, time, urllib2, logging, os
FORMAT = "%(asctime)-15s %(levelname)s %(lineno)d %(name)s \t: %(message)s"
logging.basicConfig(filename='./scout.log', filemode='w', level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)





def getElapsedTime(t ):
    return '%.2fs'%(float(time.time() - t))

def read_json_file( file):
    #path = "/Users/rrmerugu/PycharmProjects/rsquarelabs-xyz-api/lucy/configs/"

    logger.debug("Searching for configs in Path %s "%file)
    logger.debug(file)
    try:
        logger.debug(file)
        with open(file) as data_file:
            temp = data_file.read().replace('\n','').replace('\t','')
            logger.debug(temp)
            data = json.loads(temp)

            return data
    except Exception as e:
        logger.error(e)
        data = None
    return data

def read_json_from_url(url):
    try:
        response = urllib2.urlopen(url, timeout=10)
        data = json.load(response)
        logger.debug('Config file loaded Successfully :' + url)
    except Exception as e:
        logger.error(e)
        data = None
        logger.debug('Config file loading Failed :' + url)
    return data


ScrapeHTMLErrorMesg = "Unable to scrape the content"