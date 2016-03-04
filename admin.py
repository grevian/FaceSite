import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class AdminHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/admin.html')
        self.response.write(template.render({
          # TODO Fill in configuration values
        }))


    def pust(self):
        template = JINJA_ENVIRONMENT.get_template('templates/admin.html')
        self.response.write(template.render({
          # TODO Fill in configuration values
        }))
