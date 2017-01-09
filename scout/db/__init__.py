"""
'__init__.py.py' is created by 'invaana' for the project 'scout' on 14 December, 2016. 

"""
import os, sys

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DJANGO_SERVER_DIR = os.path.join(ABS_PATH, 'django_server')
sys.path.append(DJANGO_SERVER_DIR)

import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'lucy.settings'
django.setup()

from journals.models import Journal, PublicationType, PublicationKeyword

