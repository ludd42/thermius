#!/usr/bin/env python 

import os, cgi
import wsgiref.handlers 
from datetime import datetime
from google.appengine.ext import webapp

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

from model_thermius import *

class MainPage(webapp.RequestHandler):
  def get(self, page='list'):
    if page=="":
      page="list"
    inc_path = os.path.join(os.path.dirname(__file__), 'template/admin')
    template_values = {
      'this' : page,
      'header': inc_path + '/header',
      'footer': inc_path + '/footer',
      'logout_url': users.create_logout_url("http://thermius.appspot.com")
}
    if page == "add":
	  template_values["addedit"] = "Add"
    if page == "edit":
	  if self.request.get('Edit') == 'Edit':
	    template_values["addedit"] = "Edit"
	    key = self.request.get('Key')
	    flight = Flight.get(key)
	    template_values["flight"] = flight
	    template_values["key"] = key
	    page = "add"
	  if self.request.get('Delete') == 'Delete':
	    key = self.request.get('Key')
	    flight = Flight.get(key)
	    flight.delete()
	    page = "list"
    if page == "list":
      flights = db.GqlQuery("SELECT * FROM Flight ORDER BY date_launch DESC")
      template_values['flights'] = flights

    page_path = inc_path + "/%s.html" % page
    self.response.out.write(template.render(page_path, template_values))

  def post(self, lang='en', page='list'):
    if self.request.get("Cancel") != "Cancel":
      key = self.request.get('Key')
      if key == "":
	    f = Flight()
      else:
	    f = Flight.get(key)
      f.name = self.request.get('Name')
      f.date_launch = datetime.strptime(self.request.get('Date_launch'),"%Y-%m-%d %H:%M")
      f.location_launch = self.request.get('Location_launch')
      if self.request.get('Date_landed') != "":
        f.date_landed = datetime.strptime(self.request.get('Date_landed'),"%Y-%m-%d %H:%M")
      f.location_landed = self.request.get('Location_landed')
      if self.request.get('Distance') != "":
        f.distance = int(self.request.get('Distance'))
      f.notes = self.request.get('Notes')
      f.put()
	  
    self.redirect("/admin/%s" % page)


def main():
  application = webapp.WSGIApplication(
                                       [('/admin', MainPage),
                                        (r'/admin/(.*)', MainPage)
],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()