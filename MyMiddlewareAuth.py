from keystone.common import serializer
from keystone.common import wsgi
from keystone import config
from keystone import exception
from keystone.openstack.common import jsonutils
from keystone.common import logging
import 
LOG = logging.getLogger("MyMiddlewareAuth"); 
class MyMiddlewareAuth(wsgi.Middleware):
    def __init__(self, *args, **kwargs):
        super(MyMiddlewareAuth, self).__init__(*args, **kwargs)

    def process_request(self, request):
	environ = request.environ
	LOG.info('MyMiddlewareAuth')
	LOG.info(str(request.environ)); 
        if request.environ.get('REMOTE_USER', None) is not None:
            # Assume that it is authenticated upstream
            return self.application
	else:
	    return self.application;

