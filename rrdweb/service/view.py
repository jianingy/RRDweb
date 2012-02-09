from twisted.internet.threads import deferToThread
from twisted.web.server import NOT_DONE_YET
from rrdweb.service.base import BaseService
from rrdweb import rrd

import urllib
import os


class ViewService(BaseService):

    isLeaf = True

    def doViewGraph(self, request):
        from rrdweb.helper import build_view_context
        return ("view", build_view_context(request))

    def render_GET(self, request):

        d = deferToThread(self.doViewGraph, request)
        request.notifyFinish().addErrback(self.doCancel, d)
        d.addBoth(self.doResponse, request)
        return NOT_DONE_YET
