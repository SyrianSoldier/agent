from datetime import datetime


class TimeUtil:
    @classmethod
    def now_str(cls) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
