#!/usr/bin/env python

import urllib
import os
from rrdweb import rrd


def build_view_context(request):
    from rrdweb.setting import setting

    db_rel_path = "/".join(request.path.split("/")[2:])
    db_abs_path = "%s/%s" % (setting["rrd_root"], db_rel_path)

    if not os.path.isfile(db_abs_path):
        raise IOError("No such file or directory: %s" % db_abs_path)

    rrdinfo = rrd.getinfo(db_abs_path)
    ds_all = rrdinfo["ds"]

    end_time = request.args.get("end_time", ["now"])[0]
    start_time = request.args.get("start_time", ["-8h"])[0]
    width = request.args.get("width", ["600"])[0]
    height = request.args.get("height", ["150"])[0]
    title = request.args.get("title", [db_rel_path])[0]

    ds = request.args.get("ds", [])
    shape = request.args.get("shape", ["LINE2"])[0].upper()
    upper = request.args.get("lower", "0")[0]
    lower = request.args.get("upper", "0")[0]

    if ds:
        ds = list(set(filter(lambda x: x in ds_all, ds)))
    else:
        ds = ds_all.keys()

    urlparam = urllib.urlencode(dict(ds=",".join(ds),
                                     width=width,
                                     height=height,
                                     start=start_time,
                                     shape=shape,
                                     upper=upper,
                                     lower=lower,
                                     title=title,
                                     end=end_time))

    context = dict(graph=db_rel_path + "?" + urlparam,
                   up=os.path.dirname(request.path),
                   ds_all=ds_all,
                   start_time=start_time,
                   end_time=end_time,
                   width=width,
                   height=height,
                   title=title,
                   shape=shape,
                   upper=upper,
                   lower=lower,
                   ds_selected=dict([(k, 1) for k in ds]))

    return context
