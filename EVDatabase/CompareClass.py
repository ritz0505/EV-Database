import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from ReviewModel import ReviewModel

JINJA_ENVIRONMENT= jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class EVDATA(ndb.Model):
    #email address of this User
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.StringProperty()
    batterysize = ndb.StringProperty()
    wltprange=ndb.StringProperty()
    cost = ndb.StringProperty()
    power = ndb.StringProperty()

#************to compare the values of 2 EV and displaying it on the next page(compare page)*****************************
class Compare(webapp2.RequestHandler):
    def get(self):
        compid=self.request.get('compId',allow_multiple=True)
            #self.response.write(compid)
        result=[]

        for j in compid:
            comp=ndb.Key(EVDATA,j).get()
            result.append(comp)
            #self.response.write(result)

        tempcost=0
        tempbatterysize=0
        tempwltprange=0
        temppower=0
        tempyear=0
        tempcostid=None
        tempbatterysizeid=None
        tempwltprangeid=None
        temppowerid=None
        tempyearid=None
        for i in result:
            if  int(i.year)>tempyear:
                tempyear=int(i.year)
                tempyearid=i.key.id

            if  int(i.cost)>tempcost:
                tempcost=int(i.cost)
                tempcostid=i.key.id

            if int(i.wltprange)>tempwltprange:
                tempwltprange=int(i.wltprange)
                tempwltprangeid=i.key.id
            if int(i.power)>temppower:
                temppower=int(i.power)
                temppowerid=i.key.id
            if int(i.batterysize)>tempbatterysize:
                tempbatterysize=int(i.batterysize)
                tempbatterysizeid=i.key.id

                #count = count + 1
        template_values={
        'compyear':tempyearid,
        'compcost':tempcostid,
        'compbatterysize':tempbatterysizeid,
        'compwltprange':tempwltprangeid,
        'comppower':temppowerid,
        'result':result,
        }
        template = JINJA_ENVIRONMENT.get_template('Compare.html')
        self.response.write(template.render(template_values))
