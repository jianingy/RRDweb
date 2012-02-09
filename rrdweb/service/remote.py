from twisted.internet.threads import deferToThread
from twisted.web.server import NOT_DONE_YET
from rrdweb.service.base import BaseService
from twisted.python import log
import time
import os


class RemoteService(BaseService):

    isLeaf = True

    def doGetRemoteRRD(self, request):
        from rrdweb.setting import setting
        from subprocess import check_call

        relative_path = "/".join(request.path.split("/")[2:])
        hostname = os.path.dirname(relative_path)
        name = os.path.basename(relative_path)

        save_as = os.path.join(setting["rrd_root"], hostname, name)
        try:
            stat = os.stat(save_as)
            if time.time() - stat.st_mtime < setting["rrd_remote_timeout"]:
                return
        except:
            pass
        log.msg("local rrd file expired. fetching from remote %s:%s" \
                % (hostname, name))
        check_call([setting["rrd_remote"], hostname, name, save_as])

    def doView(self, args, request):

        from rrdweb.helper import build_view_context
        return ("view", build_view_context(request))

    def render_GET(self, request):
        d = deferToThread(self.doGetRemoteRRD, request)
        request.notifyFinish().addErrback(self.doCancel, d)
        d.addCallback(self.doView, request)
        d.addBoth(self.doResponse, request)
        return NOT_DONE_YET
