import os, sys
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__)) #adding the parent directory to the python path
SCOUT_PATH = os.path.join(CURRENT_PATH, '..') #adding the project to the python path
sys.path.append(SCOUT_PATH)




from scout.pubmed.parse import parse_xml_to_dict
from scout.db import Journal, PublicationKeyword, PublicationType
from django.utils.encoding import smart_str


print Journal.objects.all().count()

xmlfile = "pubmed/medsamp2016a.xml"

thedict = parse_xml_to_dict(xmlfile)
total = len(thedict)
for i, d in enumerate(thedict):
    journal_type_list = []
    for t in d['journal_type_list']:
        obj, status = PublicationType.objects.get_or_create(title=t)

        journal_type_list.append(obj)


    journal_keywords_list = []
    for kw in d['journal_keywords_list']:
        obj, status= PublicationKeyword.objects.get_or_create(title=kw)
        journal_keywords_list.append(obj)


    entry, status= Journal.objects.get_or_create(
        title= smart_str(d['title']) #.encode('utf-8'),
     )

    abstract =  d['abstract']
    try:
        if abstract:

            abstract = smart_str(d['abstract'])
        if status:
            entry.link = "https://www.ncbi.nlm.nih.gov/pubmed/%s" %d['pmid']
            entry.journal_title= smart_str(d['journal_title'])
            entry.abstract = abstract
            entry.pub_year = d['pub_year']
            entry.pub_date = d['pub_date']
            entry.pmid = d['pmid']
            entry.save()
            entry.pub_type.add(*journal_type_list)
            entry.keywords.add(*journal_keywords_list)

    except Exception as e:
        print e
    print "%s/%s - %s" %(i, total, entry)







