# 允许的域名列表
from typing import Any,Dict, List


ALLOWED_ORIGINS:List[str] = [
    "http://localhost:8000",  # 前端开发环境
    "http://example.com",     # 生产环境
    "https://example.com",    # 生产环境（HTTPS）
]

# tornado配置项
tornado_settings: Dict[str, Any] = {"port": 1080}


#
