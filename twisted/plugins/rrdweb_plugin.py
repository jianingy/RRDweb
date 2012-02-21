from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.application import internet


class Options(usage.Options):
    optParameters = [
        ["config", "c", "etc/rrdweb.yaml",
         "Configuration filename."],
        ["port", "p", 9999, "Port to listen on."],
    ]


class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)

    tapname = "rrdweb"
    description = "rrdweb"
    options = Options

    def makeService(self, options):

        from rrdweb.setting import load
        load(options["config"])

        from rrdweb import site_root
        from twisted.web import server

        site = server.Site(site_root)

        return internet.TCPServer(int(options["port"]), site)

serviceMaker = ServiceMaker()
