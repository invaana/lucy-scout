from __future__ import unicode_literals

from mongoengine import Document, EmbeddedDocument, StringField, DateTimeField, IntField, \
    ListField, EmbeddedDocumentField, connect
# Create your models here.


class PublicationType(EmbeddedDocument):
    title = StringField()


class PublicationKeyword(EmbeddedDocument):
    title = StringField()


class Tag(EmbeddedDocument):
    title = StringField()


class Journal(Document):
    title = StringField()
    journal_title = StringField()
    abstract = StringField()
    full_text = StringField()
    pub_year = IntField()
    pub_date = DateTimeField()
    pmid = IntField()
    link = StringField()
    category = StringField(max_length=20,
                           default='other',
                           choices=(
                               ('blog', 'Blog'),
                               ('website', 'Website'),
                               ('journal', 'Journal'),
                               ('book', 'Book'),
                               ('doc', 'Documentation'),
                               ('other', 'Other')
                           ))
    pub_type = ListField(EmbeddedDocumentField(PublicationType))
    keywords = ListField(EmbeddedDocumentField(PublicationKeyword))
    # tags = ListField(ReferenceField(Tag))
    source = StringField()
    image = StringField()
    pub_date_unformated = StringField()
    entry_created_at = DateTimeField()
    entry_updated_at = DateTimeField()
    meta = {
        'index_background': True,
        'index_drop_dups': True,
        'indexes': [
            'title',
            '$title',  # text index
            '#title',  # hashed index
            # 'abstract',
            # '$abstract',  # text index
            '#abstract',  # hashed index
        ]
    }
