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
        from subprocess import check_call, check_output
        from rrdweb.helper import build_view_context

        relative_path = "/".join(request.path.split("/")[2:])
        p1 = os.path.dirname(relative_path)
        p2 = os.path.basename(relative_path)

        if not p1 and not p2:
            return ("remote", dict(hostname="", items=None))

        if not p1:
            items = check_output([setting["rrd_remote"], p2]).splitlines()
            return ("remote", dict(hostname=p2, items=items))

        save_as = os.path.join(setting["rrd_root"], p1, p2)
        try:
            stat = os.stat(save_as)
            if time.time() - stat.st_mtime < setting["rrd_remote_timeout"]:
                return ("view", build_view_context(request))
            log.msg("local rrd file expired. fetching from remote %s:%s" \
                % (p1, p2))
        except:
            pass

        check_call([setting["rrd_remote"], p1, p2, save_as])

        return ("view", build_view_context(request))

    def render_GET(self, request):
        hostname = request.args.get("hostname", [""])[0]
        filename = request.args.get("filename", [""])[0]

        if hostname and filename:
            request.redirect(os.path.join("/remote", hostname, filename))
            return ""
        elif hostname:
            request.redirect(os.path.join("/remote", hostname))
            return ""

        d = deferToThread(self.doGetRemoteRRD, request)
        request.notifyFinish().addErrback(self.doCancel, d)
        d.addBoth(self.doResponse, request)
        return NOT_DONE_YET
