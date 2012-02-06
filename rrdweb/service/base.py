from twisted.web.resource import Resource
from twisted.python.failure import Failure
from twisted.python import log
from rrdweb.render import render_html
from logging import DEBUG as LVL_DEBUG

import time


class BaseService(Resource):

    def render(self, *args, **kwargs):
        self.startTime = time.time()
        return Resource.render(self, *args, **kwargs)

    def doCancel(self, err, call):
        log.msg("Cancelling current request.", level=LVL_DEBUG)
        call.cancel()

    def doResponse(self, value, request, content_type="text/html"):
        log.msg("doResposne: original value is `%s`"
                % str(value), level=LVL_DEBUG)
        request.setHeader('Content-Type', content_type)
        if isinstance(value, Failure):
            request.setResponseCode(500)
            request.write(
                render_html("error",
                            dict(message=value.value,
                                 traceback=value.getTraceback())))
        else:
            request.setResponseCode(200)
            request.write(render_html(value[0], value[1]))

        log.msg("respone time: %.3fms" % (
            (time.time() - self.startTime) * 1000))

        request.finish()
