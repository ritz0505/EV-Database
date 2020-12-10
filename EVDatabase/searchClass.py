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

#********************class to return the list of data after searching in the search page using the lower and upper range***********************
class RET(webapp2.RequestHandler):
    def get(self):
        result=''
        var=None
        action=self.request.get('Cancel')
        if action=="Cancel":
            self.redirect('/')

        #*************further function will be performed when the submit button is clicked***********************************
        if self.request.get("button"):
            ab=EVDATA.query()
            name1=self.request.get('name1',var)
            if name1:
                ab=ab.filter(EVDATA.name==self.request.get('name1'))

            manufacturer1=self.request.get('manufacturer1',var)
            if manufacturer1:
                ab=ab.filter(EVDATA.manufacturer==self.request.get('manufacturer1'))

            yearmin1=self.request.get('yearmin1',var)
            if yearmin1:
                ab=ab.filter(EVDATA.year>=self.request.get('yearmin1'))

            yearmax1=self.request.get('yearmax1',var)
            if yearmax1:
                ab=ab.filter(EVDATA.year<=self.request.get('yearmax1'))

            batterysizemin1=self.request.get('batterysizemin1',var)
            if batterysizemin1:
                ab=ab.filter(EVDATA.batterysize>=self.request.get('batterysizemin1'))

            batterysizemax1=self.request.get('batterysizemax1',var)
            if batterysizemax1:
                ab=ab.filter(EVDATA.batterysize<=self.request.get('batterysizemax1'))

            wltprangemin1=self.request.get('wltprangemin1',var)
            if wltprangemin1:
                ab=ab.filter(EVDATA.wltprange>=self.request.get('wltprangemin1'))

            wltprangemax1=self.request.get('wltprangemax1',var)
            if wltprangemax1:
                ab=ab.filter(EVDATA.wltprange<=self.request.get('wltprangemax1'))

            costmin1=self.request.get('costmin1',var)
            if costmin1:
                ab=ab.filter(EVDATA.cost>=self.request.get('costmin1'))

            costmax1=self.request.get('costmax1',var)
            if costmax1:
                ab=ab.filter(EVDATA.cost<=self.request.get('costmax1'))

            powermin1=self.request.get('powermin1',var)
            if powermin1:
                ab=ab.filter(EVDATA.power>=self.request.get('powermin1'))

            powermax1=self.request.get('powermax1',var)
            if powermax1:
                ab=ab.filter(EVDATA.power<=self.request.get('powermax1'))

            result=ab.fetch()
            if len(result)==0:
                self.response.write("There is no data for this search. Please try with other values")

        template_values={
            'result':result
        }
        action = self.request.get('button')
        #*******here if the user click on view then all the values will be rendered to next page******************
        if action == 'View':
            self.response.write(action)
            self.redirect('/EditDelete')
            template = JINJA_ENVIRONMENT.get_template('View.html')
            self.response.write(template.render(template_values))

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))
