#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.graph
import rrdweb.setting
rrdweb.setting.load("etc/rrdweb.yaml")
reload(rrdweb.service.graph)
resource = rrdweb.service.graph.GraphService()
