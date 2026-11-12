from a2wsgi import WSGIMiddleware
from main import app

application = WSGIMiddleware(app)