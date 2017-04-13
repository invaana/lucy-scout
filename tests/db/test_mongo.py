from scout.db.mongo import PublicationType, PublicationKeyword, Tag, Journal
from scout.db.mongo import connect
connect('scout')


def test_journal():
    j = Journal(title="Introduction to MD").save()
    assert j.title == "Introduction to MD"