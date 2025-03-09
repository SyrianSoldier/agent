import tornado.web
from typing_extensions import override

class BaseController(tornado.web.RequestHandler):
    @override
    def data_received(self, chunk: bytes) -> None:
        pass

    def get(self) -> None:
        self.write("HEELO,WORLD")
