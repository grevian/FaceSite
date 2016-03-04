import logging
import datetime

from google.appengine.ext import ndb

import googleapiclient
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

from models import Image

ANALYSIS_ENDPOINT = "https://vision.googleapis.com/v1/images:annotate"

credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials,
                          discoveryServiceUrl='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}')


def build_request_body(image_location):
    return [{
        'image': {
            "source": {
                "gcsImageUri": "gs://grevian-facebucket/%s" % image_location
            },
        },
        'features': [{
            'type': 'FACE_DETECTION',
            'maxResults': 10,
        }]
    }]


class ImageAnalysis(ndb.Model):
    failed = ndb.DateTimeProperty()
    started = ndb.DateTimeProperty(auto_now_add=True)
    full_result = ndb.JsonProperty()


def analyze_image(image_key_id):
    image = Image.get_by_id(int(image_key_id))
    ia = ImageAnalysis.get_by_id(int(image_key_id), parent=image.key)

    if not ia:
        raise "Attempted to start analyzing an image, but a job hasn't been created yet: %s" % image_key_id

    request = service.images().annotate(
            body={
                'requests': build_request_body(str(image.bucket_key)),
            }
    )

    try:
        response = request.execute()
    except googleapiclient.errors.HttpError as e:
        logging.warn("Failed to analyze image: %s" % e)
        ia.failed = datetime.datetime.now()
        ia.put()
        return

    logging.debug(response)

    if response["responses"][0].get("error", None):
        logging.error(response["responses"][0]["error"])
        ia.full_result = response
        ia.failed = datetime.datetime.now()
        ia.put()
        return

    ia.full_result = response
    ia.put()

