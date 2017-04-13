"""
'helpers.py' is created by 'invaana' for the project 'chatbot-ai-engine' on 14 December, 2016. 

"""

__author__ = 'rrmerugu'
import  json, time, logging
FORMAT = "%(asctime)-15s %(levelname)s %(lineno)d %(name)s \t: %(message)s"
logging.basicConfig(filename='./scout.log', filemode='w', level=logging.DEBUG, format=FORMAT)
logger = logging.getLogger(__name__)





def validate_config(config):
    """
    Validates the config file

    :param config: config file in dict format
    :return:
    """
    if config is None:
        raise ValueError("Halting the program! No config data provided")
    if type(config) is not dict:
        raise ValueError("Halting the program! Config file should be dictionary")
    if 'config' not in config.keys():
        raise ValueError("Halting the program! Invalid config format")



def getElapsedTime(t ):
    #TODO - rename the function to snake case
    return '%.2fs'%(float(time.time() - t))

def read_json_file( file):
    #path = "/Users/rrmerugu/PycharmProjects/rsquarelabs-xyz-api/lucy/configs/"
    logger.debug("Searching for configs in Path %s "%file)
    try:
        logger.debug(file)
        with open(file) as data_file:
            temp = data_file.read().replace('\n','').replace('\t','')
            data = json.loads(temp)
            return data
    except Exception as e:
        logger.error(e)
        data = None
        raise ValueError("Halting the program! Invalid file path provided")



ScrapeHTMLErrorMesg = "Unable to scrape the content"