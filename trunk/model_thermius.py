#!/usr/bin/env python 

from google.appengine.ext import db

class MailFolder(db.Model):
  date = db.DateTimeProperty(auto_now_add=True)
  subject = db.StringProperty(multiline=False)
  body = db.TextProperty()

class Flight(db.Model):
  name = db.StringProperty()
  date_launch = db.DateTimeProperty()
  location_launch = db.StringProperty(multiline=True)
  date_landed = db.DateTimeProperty()
  location_landed = db.StringProperty(multiline=True)
  distance = db.IntegerProperty()
  notes = db.TextProperty()