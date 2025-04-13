import tornado.ioloop
import tornado.web
import asyncio
from tornado.platform.asyncio import AsyncIOMainLoop

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



class TornadoApplication(tornado.web.Application):
    def __init__(self) -> None:
        tornado.web.Application.__init__(self, routes)


async def init_service() -> None:
    for Service in services:
        Service.start()



async def init_tornado_server() -> None:
      # 获取当前环境配置对象
    cur_env_config = EnvUtil.get_cur_env_config()
    LogService.runtime_logger.info(f"{cur_env_config=}")

    # 启动tornando
    app = TornadoApplication()
    app.listen(cur_env_config.get("server",{}).get("port"))



async def app_started_welcome() -> None:
    cur_env_server_config = EnvUtil.get_cur_env_config().get("server")
    host = cur_env_server_config.get("host", "localhost") #type: ignore
    port = cur_env_server_config.get("port", 1080)        #type: ignore

    LogService.runtime_logger.info(f"Server started in http://{host}:{port}")



async def init_asyncio_loop() -> None:
    """让 Tornado 使用 asyncio 的事件循环。
       实现 Tornado 与 asyncio 代码(以及基于aio的三方库,如peewee-async等)的无缝协作。
    """
    AsyncIOMainLoop().install()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(app_started_welcome())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        LogService.runtime_logger.info("Server good bye~")



async def main() -> None:
    # 初始化所有服务
    await init_service()
    await init_tornado_server()
    await init_asyncio_loop()

if __name__ == "__main__":
    asyncio.run(main())
