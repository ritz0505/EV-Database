from google.appengine.ext import ndb

class EVDATA(ndb.Model):
    #email address of this User
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.StringProperty()
    batterysize = ndb.StringProperty()
    wltprange=ndb.StringProperty()
    cost = ndb.StringProperty()
    power = ndb.StringProperty()
