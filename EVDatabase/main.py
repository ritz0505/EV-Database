import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from myuser import MyUser
from ReviewModel import ReviewModel
from AddClass import ADDEV
from searchClass import RET
from EditDeleteClass import EditDelete
from CompareClass import Compare
from ReviewSubmitClass import RevCheck
from ReviewSubmitClass import GetReview

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


class MainPage(webapp2.RequestHandler):
    def get(self):
            self.response.headers['Content-Type']='text/html'
            # URL that will contain a login or logout link
            # and also a string to represent this
            url=''
            url_string=''
            name=''
            welcome='Welcome back'
            # pull the current user from the request
            url=users.create_login_url(self.request.uri)
            url_string='login'
            user = users.get_current_user()

            if user:
                #template = JINJA_ENVIRONMENT.get_template('edittext.html')
                #self.response.write(template.render())
                url=users.create_logout_url(self.request.uri)
                url_string = 'logout'

            template_values={
            'url' :url,
            'url_string' : url_string,
            'user' : user,
            'welcome':welcome
        }
            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render())

#**********************class for option page**********************************************
class OptionButton(webapp2.RequestHandler):
    def get(self):
        action1=self.request.get('Search')
        self.response.write(action1)
        action2=self.request.get('Adddata')
        self.response.write(action2)
        action3=self.request.get('rev')
        self.response.write(action3)

        if action1=="Search":
            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render())



        if action2=="Adddata":
             self.response.write(action2)
             url=''
             url_string=''
             name=''
             welcome='Welcome back'
             # pull the current user from the request
             user = users.get_current_user()
             if user:
                 template = JINJA_ENVIRONMENT.get_template('edittext.html')
                 self.response.write(template.render())
                 url=users.create_logout_url(self.request.uri)
                 url_string = 'logout'
                 user_Details_Key = ndb.Key('MyUser', user.email())
                 user_Details = user_Details_Key.get()
                 if user_Details != None:
                     user_Details.email_address = user.email()
                     user_Details.put()
                 else:
                     user_Details = MyUser(id=user.email())
                     user_Details.email_address = user.email()
                     user_Details.put()
             else:
                 url=users.create_login_url(self.request.uri)
                 url_string='login'

             template_values={
                'url' :url,
                'url_string' : url_string,
                'user' : user,
                'welcome':welcome
             }
             template = JINJA_ENVIRONMENT.get_template('firstMainPage.html')
             self.response.write(template.render(template_values))
             #self.redirect('/')


class Checking(webapp2.RequestHandler):
    def get(self):
         url=''
         url_string=''
         name=''
         welcome='Welcome back'
             # pull the current user from the request
         url=users.create_login_url(self.request.uri)
         url_string='login'
         user = users.get_current_user()
         if user:
            template_values={
            'name':self.request.get('name'),
            'manufacturer':self.request.get('manufacturer'),
            'year':self.request.get('year'),
            'batterysize':self.request.get('batterysize'),
            'wltprange':self.request.get('wltprange'),
            'cost':self.request.get('cost'),
            'power':self.request.get('power')
           }
            template = JINJA_ENVIRONMENT.get_template('view.html')
            self.response.write(template.render(template_values))
            url=users.create_logout_url(self.request.uri)
            url_string = 'logout'
            user_Details = ndb.Key('MyUser', user.user_id())
            user_Details = user_Details.get()
            if user_Details != None:
                user_Details.email_address = user.email()
                user_Details.put()
            else:
                user_Details = MyUser(id=user.email())
                user_Details.email_address = user.email()
                user_Details.put()
         else:
            url=users.create_login_url(self.request.uri)
            url_string='login'

         template_values={
         'url' :url,
         'url_string' : url_string,
         'user' : user,
         'welcome':welcome
         }
         template = JINJA_ENVIRONMENT.get_template('firstMainPage.html')
         self.response.write(template.render(template_values))
             #self.redirect('/')

         name=self.request.get('name')
        #self.response.write(name)


         #template = JINJA_ENVIRONMENT.get_template('View.html')
         #self.response.write(template.render(template_values))

class InfoClass(webapp2.RequestHandler):
    def get(self):
        template_values={
        'name':self.request.get('name'),
        'manufacturer':self.request.get('manufacturer'),
        'year':self.request.get('year'),
        'batterysize':self.request.get('batterysize'),
        'wltprange':self.request.get('wltprange'),
        'cost':self.request.get('cost'),
        'power':self.request.get('power')
        }
        template = JINJA_ENVIRONMENT.get_template('EVInfo.html')
        self.response.write(template.render(template_values))



#*************************************Class to show all reviews to the screen*****************************
class AllReviewClass(webapp2.RequestHandler):
    def get(self):
        ab=ReviewModel.query().fetch()
        template_values={
        'ab':ab,
        'name':self.request.get('name'),
        'emailid':self.request.get('email_address'),
        'review':self.request.get('review'),
        'score':self.request.get('score')
        }
        template = JINJA_ENVIRONMENT.get_template('allreview.html')
        self.response.write(template.render(template_values))

class ShowCompare(webapp2.RequestHandler):
    def get(self):
        result=EVDATA.query().fetch()
        template_values={
        'result':result,
        'name':self.request.get('name'),
        }
        template = JINJA_ENVIRONMENT.get_template('comparedata.html')
        self.response.write(template.render(template_values))

app= webapp2.WSGIApplication([('/',MainPage),('/ADDEV',ADDEV),('/RET',RET),
('/EditDelete',EditDelete),('/Compare',Compare),('/OptionButton',OptionButton),('/InfoClass',InfoClass),('/Checking',Checking),
('/RevCheck',RevCheck),('/AllReviewClass',AllReviewClass),('/ShowCompare',ShowCompare),('/GetReview',GetReview)],debug=True)
