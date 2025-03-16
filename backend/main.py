import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload

from src.controllers import chat_controller
from src.controllers import base_controller
from config.settings import tornado_settings

# 路由表
routes: tornado.routing._RuleList = [
    (r"/", base_controller.BaseController),
    (r"/api/chat", chat_controller.ChatController)
]




# app启动后的欢迎语
def app_started_welcome() -> None:
    print(f"Tornado application started on port {tornado_settings['port']}")


class TornadoApplication(tornado.web.Application):
    def __init__(self) -> None:
        tornado.web.Application.__init__(self, routes)


def main() -> None:
    app = TornadoApplication()
    app.listen(tornado_settings["port"])
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback(callback=app_started_welcome)
    ioloop.start()


if __name__ == "__main__":
    main()
