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

#****************class to submit the review after checking the login and logout status*************************
class RevCheck(webapp2.RequestHandler):
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
            user=users.get_current_user()
            template_values={
            'name':self.request.get('name'),
            }
            template = JINJA_ENVIRONMENT.get_template('reviewpage.html')
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

class GetReview(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        myuser_key=ndb.Key('MyUser',user.email())
        myuser=myuser_key.get()
        #self.response.write(user.email())
        name=self.request.get('name')
        #self.response.write(name)
        emailId = ReviewModel.query(ReviewModel.email_address==user.email()).fetch()
        template_values={
        'name':self.request.get('name'),
        }
        if len(emailId)==0:
            rv=ReviewModel(id=user.email())
            rv.email_address=user.email()
            rv.name= self.request.get('name')
            rv.review=self.request.get('reviewtext')
            rv.score=self.request.get('score')
            rv.put()
            self.response.write("Review Submitted")
        else:
            self.response.write("A user is allowed to submit review only once.")
        #self.response.write(len(emailId))
        template = JINJA_ENVIRONMENT.get_template('reviewpage.html')
        self.response.write(template.render(template_values))
