from twisted.web.resource import Resource
from rrdweb.setting import setting
from rrdweb import rrd

import os
import time


class ViewService(Resource):

    isLeaf = True

    def render_GET(self, request):
        db_rel_path = "/".join(request.path.split("/")[2:])
        db_abs_path = "%s/%s" % (setting["RRD_ROOT"], db_rel_path)

        if not os.path.exists(db_abs_path):
            return "File not found!"

        rrdinfo = rrd.getinfo(db_abs_path)
        ds_all = rrdinfo["ds"]

        end = request.args.get("end_time", [str(int(time.time()))])[0]
        start = request.args.get("start_time",
                                 [str(int(time.time()) - 3600 * 8)])[0]
        width = request.args.get("width", ["400"])[0]
        height = request.args.get("height", ["100"])[0]
        title = request.args.get("title", os.path.splitext(db_rel_path))[0]
        ds = request.args.get("ds", None)
        shape = request.args.get("shape", ["LINE2"])[0].upper()
        upper = request.args.get("lower", "0")[0]
        lower = request.args.get("upper", "0")[0]

        if ds:
            ds = filter(lambda x: x in ds_all, ds[0].split(","))
        else:
            ds = ds_all.keys()

        request.setHeader("Content-Type", "text/plain; charset=UTF-8")

        return rrd.graph(db_abs_path, start=start, end=end,
                         width=width, height=height,
                         title=title, ds=ds, shape=shape,
                         upper=upper, lower=lower)
