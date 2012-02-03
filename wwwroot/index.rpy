#!/usr/bin/env python
# -*- mode: python -*-

import rrdweb.service.index
reload(rrdweb.service.index)
resource = rrdweb.service.index.IndexService()
