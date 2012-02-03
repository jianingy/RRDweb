setting = dict()

setting["RRD_ROOT"] = "/tmp/rrd"
setting["RRD_TOOL"] = "rrdtool"

setting["HTML_START"] = """<!DOCTYPE html>
<html>
<head>
<title>Jianing's RRD Viewer</title>
<style>
dd { display: inline; }
</style>
</head>
<body>
"""

setting["HTML_END"] = """
</body>
</html>
"""
