#!/usr/bin/env python 

import os, cgi
import wsgiref.handlers 
from google.appengine.ext import webapp

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail

from model_thermius import *

class MainPage(webapp.RequestHandler):
  def get(self, lang='en', action='index'):
    # display correct page based on language and action
    if action=="":
      action="index"
    inc_path = os.path.join(os.path.dirname(__file__), 'template/%s' % lang)
    page_path = inc_path + "/%s.html" % action
    template_values = {
      'lang': lang,
      'this' : action,
      'header': inc_path + '/header',
      'footer': inc_path + '/footer',
}
    if action == "list":
      flights = db.GqlQuery("SELECT * FROM Flight ORDER BY date_launch DESC")
      template_values['flights'] = flights

    self.response.out.write(template.render(page_path, template_values))

  def post(self, lang='en', action='index'):
    if action == "founddone":
      # save & send tracking report
      subj = "Balloon found!"
      mbody = "Date:\n"
      mbody += self.request.get('Date') + "\n\n"
      mbody += "Location:\n"
      mbody += self.request.get('Location') + "\n\n"
      mbody += "Description:\n"
      mbody += self.request.get('Desc') + "\n\n"
      mbody += "Contact:\n"
      mbody += self.request.get('Contact') + "\n\n"

    if action == "contactdone":
      # save & send contact
      subj = "Balloon Contact"
      mbody = "Name:\n"
      mbody += self.request.get('Name') + "\n\n"
      mbody += "Email:\n"
      mbody += self.request.get('Email') + "\n\n"
      mbody += "Message:\n"
      mbody += self.request.get('Message') + "\n\n"

    mail.send_mail(sender = "ludek@chovanec.com",
                   to = "ludek@chovanec.com",
                   subject = subj,
                   body = mbody.encode("utf-8")
    ) 

    #save to db
    m = MailFolder()
    m.subject = subj
    m.body = mbody
    m.put()

    self.redirect("/%s/submit" % lang)


def main():
  application = webapp.WSGIApplication(
                                       [('/', MainPage),
                                        (r'/(en|fr|bg|cz)', MainPage),
                                        (r'/(en|fr|bg|cz)/(.*)', MainPage)
],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()