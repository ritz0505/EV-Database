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

#*****************************************below class for editing and deleting the EV data*******************************
class EditDelete(webapp2.RequestHandler):
    def get(self):
        vehicle=None
        result=None
        ac=self.request.get('b1')
        self.response.write(ac)
        name=self.request.get('name')
        #self.response.write(name)
        action=self.request.get('Edit')
        action1=self.request.get('Delete')
        action2=self.request.get('Cancel')
        action3=self.request.get('view')
        self.response.write(action3)
        template_values={
        'result':result,
        'vehicle':vehicle,
        'name':self.request.get('name'),
        'manufacturer':self.request.get('manufacturer'),
        'year':self.request.get('year'),
        'batterysize':self.request.get('batterysize'),
        'wltprange':self.request.get('wltprange'),
        'cost':self.request.get('cost'),
        'power':self.request.get('power'),
        'namenew':self.request.get('namenew'),
        'manufacturernew':self.request.get('manufacturernew'),
        'yearnew':self.request.get('yearnew')
        }
        #********************code to edit the data****************************************
        if action2=="Cancel":
            self.redirect('/RET')

        if self.request.get('Edit'):
            name=self.request.get('name')
            #self.response.write(name)
            year=(self.request.get('year'))
            manufacturer=self.request.get('manufacturer')
            result_name = EVDATA.query(EVDATA.name==self.request.get('namenew'),
            EVDATA.manufacturer==self.request.get('manufacturernew'),EVDATA.year==self.request.get('yearnew')).fetch()


            if len(result_name)==0:
                id=name+""+manufacturer+""+year

                dbs=ndb.Key('EVDATA',str(id)).get()
                self.response.write(dbs)
                dbs.key.delete()

                RVS= EVDATA(id=""+self.request.get('namenew')+""+self.request.get('manufacturernew')+""+self.request.get('yearnew'))
                #rv.EVDATA()
                #rv.id='bmwritika2222'
                RVS.name=self.request.get('namenew')
                RVS.manufacturer= self.request.get('manufacturernew')
                RVS.year=self.request.get('yearnew')
                RVS.batterysize=self.request.get('batterysize')
                RVS.wltprange=self.request.get('wltprange')
                RVS.cost=self.request.get('cost')
                RVS.power=self.request.get('power')
                RVS.put()
                self.response.write(id)
                self.redirect('/RET')
            else:
                self.response.write('Name, Manufacturer, year should be unique. Data already exists.')
        #*****************code to delete the data****************************************************
        elif action1 =='Delete':
                name=self.request.get('name')
                year=(self.request.get('year'))
                manufacturer=self.request.get('manufacturer')
                result = EVDATA.query(
                EVDATA.name==self.request.get('namenew'),
                EVDATA.manufacturer==self.request.get('manufacturernew'),
                EVDATA.year==self.request.get('yearnew')
                ).fetch()
                id=name+""+manufacturer+""+year
                dbs=ndb.Key('EVDATA',str(id)).get()
                self.response.write(dbs)
                dbs.key.delete()
                self.response.write("Data Deleted Successfully.")
                self.redirect('/RET')


        template = JINJA_ENVIRONMENT.get_template('View.html')
        self.response.write(template.render(template_values))
        url=users.create_logout_url(self.request.uri)
        url_string = 'logout'
