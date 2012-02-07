import re

REGEX_DS = re.compile("^ds\[([^]]+)\]\.([^=]+)=(.+)")


def run_rrdtool(command, option, rrd):
    from subprocess import check_output, STDOUT
    from rrdweb.setting import setting

    command = [setting["rrd_tool"], command, rrd]
    command.extend(option)
    return check_output(command, stderr=STDOUT)


def colors(n):
    from colorsys import hsv_to_rgb

    for x in xrange(n):
        rgb = list(hsv_to_rgb(x * 1.0 / n, 0.5, 0.8))
        rgb[0] = "%x" % int(rgb[0] * 256)
        rgb[1] = "%x" % int(rgb[1] * 256)
        rgb[2] = "%x" % int(rgb[2] * 256)
        yield "".join(rgb)


def getinfo(db_path):
    ds = dict()
    data = run_rrdtool("info", "", db_path)
    if data:
        for line in data.splitlines():
            match = REGEX_DS.match(line)
            if match:
                dsname = match.group(1)
                if dsname not in ds:
                    ds[dsname] = dict()
                ds[dsname][match.group(2).strip()] = match.group(3).strip()
    return dict(ds=ds)


def graph(db_path, **kw):
    option = []

    option.extend(("--start", kw["start"]))
    option.extend(("--end", kw["end"]))

    option.extend(("--width", kw["width"]))
    option.extend(("--height", kw["height"]))

    option.extend(("--upper", kw["upper"]))
    option.extend(("--lower", kw["lower"]))

    c = colors(len(kw["ds"]))
    for ds in kw["ds"]:
        color = c.next()
        option.append("DEF:%s=%s:%s:AVERAGE"
                      % (ds.replace("-", "_"), db_path, ds))
        if kw["shape"] == "AREA":
            stack = ":STACK"
        else:
            stack = ""
        option.append("%s:%s#%s:%s%s"
                      % (kw["shape"], ds.replace("-", "_"), color, ds, stack))
        option.append("GPRINT:%s:LAST:LAST \:%%4.2lf %%S " % (ds))
        option.append("GPRINT:%s:AVERAGE:AVERAGE \:%%4.2lf %%S \\r" % (ds))

    return run_rrdtool("graph", option, "-")
