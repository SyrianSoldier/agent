import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from typing_extensions import Any

from src.controllers import base_controller

# 路由表
routes: tornado.routing._RuleList = [
    (r"/", base_controller.BaseController),
]

# tornado配置项
tornado_settings: dict[str, Any] = {"port": 1080}


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
