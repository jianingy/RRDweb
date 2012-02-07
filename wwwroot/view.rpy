#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.view
import rrdweb.setting
rrdweb.setting.load("etc/rrdweb.yaml")
reload(rrdweb.service.view)
resource = rrdweb.service.view.ViewService()
