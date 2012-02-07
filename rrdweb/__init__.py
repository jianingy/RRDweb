from twisted.web.resource import Resource
from twisted.web.static import File
from rrdweb.service.index import IndexService
from rrdweb.service.view import ViewService
from rrdweb.service.graph import GraphService
from rrdweb.service.list import ListService

site_root = Resource()
site_root.putChild("", IndexService())
site_root.putChild("static", File("static"))
site_root.putChild("view", ViewService())
site_root.putChild("graph", GraphService())
site_root.putChild("list", ListService())
