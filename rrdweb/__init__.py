from twisted.web.resource import Resource
from twisted.web.static import File
from rrdweb.service.index import IndexService
from rrdweb.service.view import ViewService
from rrdweb.service.graph import GraphService
from rrdweb.service.local import LocalService
from rrdweb.service.remote import RemoteService

site_root = Resource()
site_root.putChild("", IndexService())
site_root.putChild("status.taobao", File("status.taobao"))
site_root.putChild("static", File("static"))
site_root.putChild("view", ViewService())
site_root.putChild("graph", GraphService())
site_root.putChild("local", LocalService())
site_root.putChild("remote", RemoteService())
