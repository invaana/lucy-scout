"""
'mongo.py' is created by 'invaana' for the project 'scout' on 14 December, 2016. 

"""

from mongoengine import StringField, DateTimeField, ListField, DictField, Document, connect
import datetime


connect('scout')

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

    # meta = {
    #     'indexes': [
    #         {'fields': ['-link'], 'unique': True,
    #          'sparse': True, 'types': False},
    #     ],
    # }

    def save(self, *args, **kwargs):
        self.date = datetime.datetime.now()
        super(ScrapedData, self).save(*args, **kwargs)



"""

# class ScrapedData(Document):
#     title = StringField(required=True, max_length=200)
#     posted = DateTimeField(default=datetime.datetime.now)
#     tags = ListField(StringField(max_length=50))
#     meta = {'allow_inheritance': True}
#
#
#
#
#
#
#
# class ScraperLink(Document):
#     scraper_id = AutoField(primary_key=True)
#     scraper_config = TextField()
#     time =  DateTimeField(auto_now_add=True)
#
#
#
# class ScrapedTags(models.Model):
#     tag_id = models.AutoField(primary_key=True)
#     title = StringField(max_length=100)
#     slug = models.SlugField( )
#     entry =  models.ForeignKey('ScrapedData',related_name= 'tags')
#     def __unicode__(self):
#         return self.title
#
#
# class ScrapedCategories(models.Model):
#     cat_id = models.AutoField(primary_key=True)
#     title = StringField(max_length=100,   default="")
#     slug = models.SlugField( )
#     entry = models.ForeignKey('ScrapedData', related_name='categories')
#     def __unicode__(self):
#         return self.title
#
# class ScrapedImages(models.Model):
#     image_id = models.AutoField(primary_key=True)
#     image_url = StringField(max_length=500)
#     entry = models.ForeignKey('ScrapedData', related_name='images')
#     def __unicode__(self):
#         return "%s" %self.image_url
#


"""