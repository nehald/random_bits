from keystone.common import serializer
from keystone.common import wsgi
from keystone import config
from keystone import exception
from keystone.openstack.common import jsonutils
from keystone.common import logging
import pdb 



class vom_auth(wsgi.Middleware):
    def process_request(self, request):
	pdb.set_trace(); 
        if request.environ.get('REMOTE_USER', None) is not None:
            # Assume that it is authenticated upstream
            return self.application
	else:
	    return self.application;
