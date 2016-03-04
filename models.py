from google.appengine.ext import ndb


class Image(ndb.Model):
    bucket_key = ndb.StringProperty(indexed=False, required=True)
    display_url = ndb.StringProperty(indexed=True, required=True)
    thumbnail_url = ndb.StringProperty(indexed=False, required=True)
    uploaded = ndb.DateTimeProperty(auto_now_add=True, required=True)

    @property
    def id(self):
        return self.key.id()



