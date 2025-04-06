from src.service.log_service import LogService
import logging

class TestLog:
    @classmethod
    def setup_class(cls) -> None:
        LogService().start()

    @classmethod
    def teardown_class(cls) -> None:
        pass

    def test_color_output(self) -> None:
        """测试向控制台输出彩色log"""
        logger = logging.getLogger(__name__)

        logger.debug("debug")
        logger.info("info")
        logger.warning("warning")
        logger.error("error")


