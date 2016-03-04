import webapp2
import jinja2
import os
import logging

from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url_async
from google.appengine.ext.ndb import Future

from models import Image

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
            blob_key = upload.key()

            # Generate a Thumbnail and inline displayable sized image
            thumbnail_url_future = get_serving_url_async(blob_key, size=120)
            display_url_future = get_serving_url_async(blob_key, size=480)
            Future.wait_all([display_url_future, thumbnail_url_future])

            # Store the image metadata
            i = Image(
                bucket_key=str(blob_key),
                display_url=display_url_future.get_result(),
                thumbnail_url=thumbnail_url_future.get_result()
            )
            i.put()

            self.redirect('/gallery/%s' % i.key.id())
        except Exception as e:
            logging.error(e)
            self.error(500)
