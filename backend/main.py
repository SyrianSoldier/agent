import tornado.ioloop
import tornado.web
import asyncio

from typing_extensions import List,Type, Any, Dict

from src.controllers import chat_controller
from src.controllers import base_controller

from src.service.base_service import BaseService
from src.service.db_service import DBService
from src.service.log_service import LogService

from src.util.env_util import EnvUtil

# 路由表
routes: tornado.routing._RuleList = [
    (r"/", base_controller.BaseController),
    (r"/api/chat", chat_controller.ChatController)
]

#Services
services:List[Type[BaseService]] = [
    DBService,
    LogService
]


# app启动后的欢迎语
def app_started_welcome() -> None:
    cur_env_server_config = EnvUtil.get_cur_env_config().get("server")
    host = cur_env_server_config.get("host", "localhost") #type: ignore
    port = cur_env_server_config.get("port", 1080)        #type: ignore

    LogService.runtime_logger.info(f"Server started in http://{host}:{port}")
    print(f"Server started in http://{host}:{port}")


class TornadoApplication(tornado.web.Application):
    def __init__(self) -> None:
        tornado.web.Application.__init__(self, routes)


def init_service() -> None:
    for Service in services:
        Service().start()


def main() -> None:
    # 初始化所有服务
    init_service()

    # 获取当前环境配置对象
    cur_env_config = EnvUtil.get_cur_env_config()
    LogService.runtime_logger.info(f"{cur_env_config=}")

    # 启动tornando
    app = TornadoApplication()
    app.listen(cur_env_config.get("server",{}).get("port"))
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback(callback=app_started_welcome)
    ioloop.start()


if __name__ == "__main__":
    main()
