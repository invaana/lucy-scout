"""
'settings.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.

"""


"""
Settings based on
http://docs.celeryproject.org/en/latest/getting-started/introduction.html#celery-is
"""
import os
from celery import Celery
worker = Celery('scout', broker='redis://localhost:6379/0')




CONFIG_DIR = "."
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
