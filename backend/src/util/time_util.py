from datetime import datetime, timezone
from zoneinfo import ZoneInfo  # Python 3.9+ 自带

class TimeUtil:
    default_time_format: str = "%Y-%m-%d %H:%M:%S"
    shanghai_tz = ZoneInfo("Asia/Shanghai")  # 上海时区对象

    @classmethod
    def now_str(cls, format_: str|None = None) -> str:
        """获取本地时间的格式化字符串"""
        return datetime.now().strftime(format_ or cls.default_time_format)


    @classmethod
    def now_utc(cls, format_: str|None = None, isoformat: bool = False) -> str:
        """获取UTC时间的字符串表示"""
        utc_now = datetime.now(timezone.utc)

        if isoformat is True:
            return utc_now.isoformat()
        return utc_now.strftime(format_ or cls.default_time_format)


    @classmethod
    def now_shanghai(cls, format_: str|None = None, isoformat: bool = False) -> str:
        """获取上海当前时间的字符串"""
        shanghai_time = datetime.now(cls.shanghai_tz)

        if isoformat is True:
            return shanghai_time.isoformat()
        return shanghai_time.strftime(format_ or cls.default_time_format)


    @classmethod
    def utc_to_shanghai(cls, time_str: str, format_: str|None = None, src_format:str|None = None, isoformat:bool=False) -> str:
        """将UTC时间字符串转换为上海时间

        :param time_str: UTC时间字符串
        :param src_format: 源时间格式，默认自动检测
        """
        if src_format is None:
            if "T" in time_str:  # ISO格式
                dt = datetime.fromisoformat(time_str)
            else:
                dt = datetime.strptime(time_str, cls.default_time_format).replace(tzinfo=timezone.utc)
        else:
            dt = datetime.strptime(time_str, src_format).replace(tzinfo=timezone.utc)

        # 转换为上海时区
        shanghai_time = dt.astimezone(cls.shanghai_tz)

        if isoformat is True:
            return shanghai_time.isoformat()
        return shanghai_time.strftime(format_ or cls.default_time_format)
