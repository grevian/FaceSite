import datetime
import webapp2
import logging
import json

from google.appengine.ext import ndb

TIMEOUT = datetime.timedelta(minutes=5)


def expired(start_time):
    duration = start_time - datetime.datetime.now()
    return duration > TIMEOUT


class PollAnalysisHandler(webapp2.RequestHandler):
    def get(self, image):
        self.response.headers['Content-Type'] = 'application/json'

        image_id = int(image)
        ia_key = ndb.Key('Image', image_id, 'ImageAnalysis', image_id)
        ia = ia_key.get()

        if not ia:
            self.abort(404)

        if not ia.failed and not ia.completed and expired(ia.started):
            logging.warn("Timing out analysis job, marking it failed. %s" % id)
            ia.failed = datetime.datetime.now()
            ia.put()

        if ia.completed or ia.failed:
            # Its status wont change after this, cache the results forever
            self.response.cache_control = 'public'
            self.response.cache_control.max_age = 300

        if ia.full_result:
            self.response.out.write(json.dumps(ia.full_result))
        else:
            self.response.out.write(json.dumps({"status": "pending"}))
