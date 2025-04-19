import tornado.web
import asyncio
from src.util.env_util import EnvUtil

from src.service.log_service import LogService

from src.routes import routes
from src.service import services


class TornadoApplication(tornado.web.Application):
    def __init__(self) -> None:
        super().__init__(routes)


async def init_service() -> None:
    for Service in services:
        await Service.start()


async def init_tornado_server() -> None:
    cur_env_config = EnvUtil.get_cur_env_config()
    app = TornadoApplication()
    app.listen(cur_env_config.get("server", {}).get("port"))


async def app_started_welcome() -> None:
    cur_env_server_config = EnvUtil.get_cur_env_config().get("server")
    host = cur_env_server_config.get("host", "localhost")  # type: ignore
    port = cur_env_server_config.get("port", 1080)         # type: ignore
    LogService.runtime_logger.info(f"Server started at http://{host}:{port}")


async def main() -> None:
    await init_service()
    await init_tornado_server()
    await app_started_welcome()

    # 保持事件循环运行
    # see: https://github.com/tornadoweb/tornado/blob/stable/demos/chat/chatdemo.py
    #      https://docs.python.org/3/library/asyncio-sync.html#asyncio.Event
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
