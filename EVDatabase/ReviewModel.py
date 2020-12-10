from google.appengine.ext import ndb
class ReviewModel(ndb.Model):
    #email address of this User\
    name=ndb.StringProperty()
    email_address = ndb.StringProperty()
    review=ndb.StringProperty()
    score=ndb.StringProperty()
