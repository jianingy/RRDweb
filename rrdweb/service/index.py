from twisted.web.resource import Resource
from mako.template import Template
from rrdweb.setting import setting
from rrdweb import rrd
import os


class IndexService(Resource):

    isLeaf = True

    def render_GET(self, request):
        rel_path = "/".join(request.path.split("/")[2:])
        abs_path = "%s/%s" % (setting["RRD_ROOT"], rel_path)

        if not os.path.isdir(abs_path):
            return "Directory not found!"

        Template(filename="
        html = []

        html.append("<dl>")
        if rel_path:
            dt  = "<dt><a href=\"%s\">..</a></dt>" \
                % (os.path.dirname(request.path))
            html.append(dt)
        for entry in os.listdir(abs_path):
            if os.path.isdir(abs_path + "/" + entry):
                dt  = "<dt><a href=\"%s/%s\">%s</a></dt>" \
                    % (request.path, entry, entry)
                html.append(dt)
            else:
                db_abs_path = "%s/%s" % (abs_path, entry)
                rrdinfo = rrd.getinfo(db_abs_path)
                ds_all = rrdinfo["ds"]
                dt = "<dt>%s</dt>" % entry
                html.append(dt)
                dd = "<dd><a href=\"/view.rpy/%s/%s\">all</a></dd>" \
                    % (rel_path, entry)
                html.append(dd)
                for ds in ds_all.keys():
                    dd = "<dd><a href=\"/view.rpy/%s/%s?ds=%s\">%s</a></dd>" \
                        % (rel_path, entry, ds, ds)
                    html.append(dd)

        html.append("</dl>")
        return "\n".join([setting["HTML_START"],
                          "\n".join(html),
                          setting["HTML_END"]])
