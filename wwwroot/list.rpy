#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.list
reload(rrdweb.service.list)
resource = rrdweb.service.list.ListService()
