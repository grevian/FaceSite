import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/gallery.html')
        self.response.write(template.render({
        }))

class ImageHandler(webapp2.RequestHandler):
    def get(self, image):
        template = JINJA_ENVIRONMENT.get_template('templates/image.html')
        self.response.write(template.render({
        'img_src': image
        }))

class Main(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/landing.html')
        self.response.write(template.render({
        }))

