import logging
import webapp2
import jinja2
import os

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

        i = Image.get_by_id(int(image))

        if not i:
            img_url = "/img/missing.png"
            logging.warn("Could not find image %s", image)
        else:
            img_url = i.display_url

        template = JINJA_ENVIRONMENT.get_template('templates/image.html')
        self.response.write(template.render({
            'img_src': img_url
        }))


class Main(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/landing.html')
        self.response.write(template.render({
        }))

