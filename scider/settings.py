"""
'settings.py' is created by 'invaana' for the project 'scout' on 14 December, 2016.

"""


"""
Settings based on
http://docs.celeryproject.org/en/latest/getting-started/introduction.html#celery-is
"""

from celery import Celery
worker = Celery('scider', broker='amqp://guest@localhost//')



