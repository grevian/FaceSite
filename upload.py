import datetime
import webapp2
import jinja2
import os

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class UploadHandler(webapp2.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/upload/completed', gs_bucket_name="grevian-facebucket")
    
        template = JINJA_ENVIRONMENT.get_template('templates/upload.html')
        self.response.write(template.render({
          'upload_url': upload_url
        }))

class GCSUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            upload = self.get_uploads()[0]
            blob_key=upload.key()
            self.redirect('/gallery/%s' % blob_key)
        except:
            self.error(500)
