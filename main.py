import webapp2
from admin import AdminHandler
from gallery import GalleryHandler, ImageHandler, Main
from upload import UploadHandler, GCSUploadHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', Main),
    webapp2.Route('/admin', AdminHandler, name="admin"),
    webapp2.Route('/gallery', GalleryHandler, name="gallery"),
    webapp2.Route('/gallery/<image:.+>', ImageHandler, name="image"),
    webapp2.Route('/upload', UploadHandler, name="upload"),
    webapp2.Route('/upload/completed', GCSUploadHandler, name="gcs_upload"),
], debug=True)
