from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Journal(models.Model):
    """
    Model  created  with fields

    """
    title = models.CharField(max_length=1000, db_index=True)
    journal_title = models.CharField(max_length=120, db_index=True)
    abstract = models.TextField(null=True, blank=True)
    pub_year = models.IntegerField(null=True, blank=True)
    pub_date = models.DateTimeField(null=True, blank=True)
    pmid = models.IntegerField(null=True, blank=True)
    link = models.CharField(max_length=200, null=True)

    pub_type = models.ManyToManyField('PublicationType', )
    keywords = models.ManyToManyField('PublicationKeyword')

    def __str__(self):
        """
         Returns the Journal title
        """
        return self.title

class PublicationType(models.Model):
    """
    PublicationType for the Journal
    """
    title = models.CharField(max_length=150, db_index=True)

    def __str__(self):
        return self.title

class PublicationKeyword(models.Model):
    """
    PublicationKeyword for the Journal
    """
    title = models.CharField(max_length=150, db_index=True)
    def __str__(self):
        return self.title