from rrdweb.service.base import BaseService


class IndexService(BaseService):

    def render_GET(self, request):
        request.redirect("/local")
        return "Redirect to /local"
