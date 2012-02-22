from twisted.web.server import NOT_DONE_YET
from twisted.internet.threads import deferToThread
from rrdweb.service.base import BaseService
from rrdweb import rrd
import os


class LocalService(BaseService):

    isLeaf = True

    def doListDirectory(self, request):
        from rrdweb.setting import setting

        relative_path = "/".join(request.path.split("/")[2:]).rstrip("/")
        absolute_path = "%s/%s" % (setting["rrd_root"], relative_path)
        entries = []

        if not os.path.isdir(absolute_path):
            raise IOError("No such file or directory: %s" % absolute_path)

        for entry in os.listdir(absolute_path):

            if os.path.isdir(os.path.join(absolute_path, entry)):
                entries.append(dict(href=os.path.join(request.path, entry),
                                    text=entry))
            else:
                db_path = os.path.join(absolute_path, entry)
                try:
                    ds_all = rrd.getinfo(db_path)["ds"]
                    href = os.path.join("/view", relative_path, entry)
                    subitems = [dict(href=href, text="all")]
                    for ds in ds_all.keys():
                        href = os.path.join("/view", relative_path, entry)
                        href += "?ds=%s" % ds
                        subitems.append(dict(href=href, text=ds))
                except:
                    subitems = []

                entries.append(
                    dict(href=os.path.join("/view", relative_path, entry),
                         text=entry,
                         subitems=subitems))
        return ("local", dict(entries=entries,
                             up=os.path.dirname(request.path.lstrip("/"))))

    def render_GET(self, request):

        d = deferToThread(self.doListDirectory, request)
        request.notifyFinish().addErrback(self.doCancel, d)
        d.addBoth(self.doResponse, request)
        return NOT_DONE_YET
