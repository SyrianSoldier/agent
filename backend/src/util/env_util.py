import os
import json
from typing_extensions import Dict, Literal, cast, Optional, Any



class EnvUtil:
    @classmethod
    def _get_config_dir(cls) -> str:
        """获取config目录的根目录"""
        current_file_path:str = os.path.abspath(__file__)
        current_dir = os.path.dirname(current_file_path)

        return os.path.join(current_dir, "..", "..", "config" )


    @classmethod
    def get_cur_env(cls) -> Literal["dev", "prev", "prod"]:
        """获取当前环境"""
        env:Optional[str] = os.getenv("agent_env")
        if env not in {"dev", "prev", "prod"}:
            env = "dev"

        return cast(Literal["dev", "prev", "prod"], env)

    @classmethod
    def convert_env_config(cls, origin_config: dict[str, Any]) -> dict[str, Any]:
        """处理配置文件, 优先从配置文件中读取主机地址/数据库用户名/密码/端口号等, 如果为 "env" 则尝试从环境变量中读取"""
        env = "agent_" + cls.get_cur_env()

        db_config: dict[str, Any] = origin_config.get("database", {}).copy()

        for key, value in db_config.items():
            if key.lower() == "host" and isinstance(value, str) and value.lower() == "env":
                host: str | None = os.getenv(f"{env}_database_host")
                if host is None:
                    raise Exception(f"环境变量 {env}_database_host 未设置")
                db_config["host"] = host

            elif key.lower() == "port" and isinstance(value, str) and value.lower() == "env":
                port: str | None = os.getenv(f"{env}_database_port")
                if port is None:
                    raise Exception(f"环境变量 {env}_database_port 未设置")
                db_config["port"] = int(port)

            elif key.lower() == "user" and isinstance(value, str) and value.lower() == "env":
                user: str | None = os.getenv(f"{env}_database_user")
                if user is None:
                    raise Exception(f"环境变量 {env}_database_user 未设置")
                db_config["user"] = user

            elif key.lower() == "password" and isinstance(value, str) and value.lower() == "env":
                password: str | None = os.getenv(f"{env}_database_password")
                if password is None:
                    raise Exception(f"环境变量 {env}_database_password 未设置")
                db_config["password"] = password

        return {**origin_config, "database": db_config}


    @classmethod
    def get_cur_env_config(cls) -> Dict[str, Any]:
        """获取当前环境的配置对象"""
        cur_env = cls.get_cur_env()

        base_config_path:str = os.path.join(
            cls._get_config_dir(),
            "base_config.json"
        )

        with open(base_config_path, "r", encoding="utf-8") as f:
            base_config = json.load(f)

        env_config_path = ""
        if cur_env == "dev":
            env_config_path = os.path.join(
                cls._get_config_dir(),
                "dev_config.json"
            )
        elif cur_env == "prev":
            env_config_path = os.path.join(
                cls._get_config_dir(),
                "prev_config.json"
            )
        elif cur_env == "prod":
            env_config_path = os.path.join(
                cls._get_config_dir(),
                "prod_config.json"
            )


        with open(env_config_path, "r", encoding="utf-8") as f:
            env_config = json.load(f)

        return {**base_config, **cls.convert_env_config(env_config)}
