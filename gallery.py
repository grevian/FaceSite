import logging
import webapp2
import jinja2
import json
import os

from google.appengine.ext import ndb
from google.appengine.ext.ndb import Cursor

from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        cursor = self.request.get("cursor", None)
        if cursor:
            cursor = Cursor(urlsafe=cursor)
        ctx = {}

        image_q = Image.query().order(-Image.uploaded)
        image_list, next_curs, more = image_q.fetch_page(20, start_cursor=cursor)

        ctx['images'] = list(image_list)

        if more:
            ctx['cursor'] = next_curs.urlsafe()

        template = JINJA_ENVIRONMENT.get_template('templates/gallery.html')
        self.response.write(template.render(ctx))


class ImageHandler(webapp2.RequestHandler):
    def get(self, image):
        ctx = {}

        image_key = ndb.Key('Image', int(image))
        annotation_key = ndb.Key('Image', int(image), 'ImageAnalysis', int(image))
        annotation_future = annotation_key.get_async()

        i = image_key.get()

        if not i:
            ctx['img_src'] = "/img/missing.png"
            logging.warn("Could not find image %s", image)
        else:
            ctx['img_src'] = i.display_url

        ia = annotation_future.get_result()

        if ia:
            try:
                ia_data = {}
                annotations = ia.full_result["responses"][0]["faceAnnotations"][0]
                for a in ("angerLikelihood", "joyLikelihood", "sorrowLikelihood", "surpriseLikelihood",
                          "headwearLikelihood", "detectionConfidence", "blurredLikelihood", "underExposedLikelihood"):
                    ia_data[a] = annotations[a]
                ctx['img_annotation'] = ia_data
            except Exception as e:
                logging.warn("Failed to unpack annotations, %s" % e)
                ctx['img_annotation'] = {}
            finally:
                ctx['full_results'] = json.dumps(ia.full_result)

        template = JINJA_ENVIRONMENT.get_template('templates/image.html')
        self.response.write(template.render(ctx))


class Main(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/landing.html')
        self.response.write(template.render({
        }))

