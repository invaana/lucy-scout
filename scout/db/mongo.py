"""
'mongo.py' is created by 'invaana' for the project 'scout' on 14 December, 2016. 

"""

from mongoengine import StringField, DateTimeField, ListField, DictField, Document, connect
import datetime




class ScrapedData(Document):
    link = StringField(max_length=500)
    title = StringField(max_length=300)
    html = StringField()
    domain = StringField(max_length=200)
    image = StringField(max_length=500)

    # entry date in blog
    published_date = DateTimeField()
    published_date_unformated = StringField()
    date =  DateTimeField(db_field='addDate',default=datetime.datetime.now)

    def __unicode__(self):
        return "%s" %( self.link)

    meta = {
        'indexes': [
            {'fields': ['-link'], 'unique': True,
             'sparse': True,  },
        ],
    }

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super(ScrapedData, self).save(*args, **kwargs)

