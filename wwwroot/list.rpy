#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.list
import rrdweb.setting
rrdweb.setting.load("etc/rrdweb.yaml")
reload(rrdweb.service.list)
resource = rrdweb.service.list.ListService()
