#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.view
reload(rrdweb.service.view)
resource = rrdweb.service.view.ViewService()
