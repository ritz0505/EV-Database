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


#************class to add EV data**************************************************
class ADDEV(webapp2.RequestHandler):
    def get(self):
        vehicle = EVDATA.query()
        result= list(vehicle.fetch())
        print('ala')
        print(result)
        user=''
        url=''
        url_string=''
        welcome=''
        template_values={
        'result' :result
        }
        #*****checking the existing data in the below code*************
        name_val = EVDATA.query(EVDATA.name==self.request.get('name'))
        vehicle1=name_val.fetch()
        manu_val=EVDATA.query(EVDATA.manufacturer==self.request.get('manufacturer'))
        vehicle2=manu_val.fetch()
        year_val=EVDATA.query(EVDATA.year==self.request.get('year'))
        vehicle3=year_val.fetch()

        #***********if data doesnot exists then only it will put the data in the datastore*****************
        if len(vehicle1)==0 and len(vehicle2)==0 and len(vehicle3)==0:
            #self.response.write('populating<br/>')
            rv=EVDATA(id=self.request.get('name')+""+self.request.get('manufacturer')+""+self.request.get('year'))
            rv.name= self.request.get('name')
            rv.manufacturer= self.request.get('manufacturer')
            rv.year=self.request.get('year')
            rv.batterysize=self.request.get('batterysize')
            rv.wltprange=self.request.get('wltprange')
            rv.cost=self.request.get('cost')
            rv.power=self.request.get('power')
            rv.put()
            #template = JINJA_ENVIRONMENT.get_template('edittext.html')
            #self.response.write(template.render())
            self.response.write("Data has been added successfully.")

        else:
            self.response.write("Data Already exists. Name, Manufacturer, year should be unique." )
