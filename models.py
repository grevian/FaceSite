from google.appengine.ext import ndb

class Image(ndb.Model):
    bucket_key = ndb.StringProperty(indexed=False, required=True)
    name = ndb.StringProperty(required=True)
    uploaded = ndb.DateTimeProperty(auto_now_add=True)


