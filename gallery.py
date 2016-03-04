import logging
import webapp2
import jinja2
import os

from google.appengine.ext import ndb

from models import Image

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        image_list = Image.query().order(-Image.uploaded).fetch(20)

        template = JINJA_ENVIRONMENT.get_template('templates/gallery.html')
        self.response.write(template.render({
            'images': list(image_list)
        }))


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

        template = JINJA_ENVIRONMENT.get_template('templates/image.html')
        self.response.write(template.render(ctx))


class Main(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/landing.html')
        self.response.write(template.render({
        }))

