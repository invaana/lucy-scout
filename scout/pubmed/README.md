



## How to use

```python 
from scout.pubmed.parse import parse_xml_to_dict

thedict_list = parse_xml_to_dict()
for i,d in enumerate(thedict_list):
    pass

```

```json

// structure of d
d = {
    'pmid': pmid,
    'title': title,
    'journal_title': journal_title,
    'abstract': abstract,
    'pub_year': journal_year, # integer
    'pub_date': journal_pubdate, # datetime object
    'journal_keywords_list': journal_keywords, # list
    'journal_type_list': journal_type, #2 list

}

```