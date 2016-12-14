# -*- coding: utf-8 -*-

"""
'clean.py' is created by 'invaana' for the project 'scout' on 14 December, 2016. 

"""


from bs4 import BeautifulSoup

from lxml.html.clean import Cleaner
from lxml.html import fromstring
from lxml.html import _transform_result
import htmlmin

cleaner = Cleaner()
cleaner.javascript = True # This is True because we want to activate the javascript filter
cleaner.style = True      # This is True because we want to activate the styles & stylesheet filter



def clean_html(html_content=None):

    """
    This method takes url as inputs and outputs the plane html without dirty classes,
    <script>, <style> tags

    :param url: a valid url,
    :return:
    """
    if html_content is None:
        raise "Valid Html content should be parsed "

    clean_html =   cleaner.clean_html(html_content)
    doc = fromstring(clean_html)
    TO_CLEAN_TAGS = ['div','li','ul','h1','h2','h3','h4','h5','h6','p','a','img',
                     'span','code', 'pre', 'ol','li', 'dl', 'section','nav']
    TO_REMOVE_ATTR = ['class','title','rel','alt','height','width','id','accesskey']

    """
    id is an important attribute, sometimes it links the two things, but pointing as
    link
    """
    # TO_EXCEPT_IDS = ['a', 'div']
    TO_REMOVE_BLANK_TAGS = ['div','section','span','a','body']

    for tag in TO_CLEAN_TAGS:
        for el in doc.iter(tag):
            # if tag not in TO_EXCEPT_IDS:
            #     if "id" in el.attrib:
            #         del el.attrib['id']

            if 'href' in el.attrib:
                if el.attrib['href'].startswith('#'):
                    del el.attrib['href']

            for ex in TO_REMOVE_ATTR:
                if ex in el.attrib:
                    del el.attrib[ex]

    final_cleaned_html =  _transform_result(type(clean_html), doc)

    final_cleaned_html=final_cleaned_html.replace('¶','') # replacing paragraph symbols
    soup = BeautifulSoup(final_cleaned_html,'lxml')
    final_cleaned_html = soup.body.encode("utf-8")
    elements = soup.find_all(True)

    for el in elements:
        if len(el.text) == 0:
            el.extract()

    for tag in TO_REMOVE_BLANK_TAGS:
        final_cleaned_html = final_cleaned_html.replace("<%s>"%tag,'').replace('</%s>'%tag,'').replace("\n","")

    final_cleaned_html = htmlmin.minify(unicode(final_cleaned_html, 'unicode-escape'))

    return final_cleaned_html

