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
        env:Optional[str] = os.getenv("AGENT_ENV") # 在预发机器和线上机器上需要手动注入环境变量

        if env not in {"dev", "prev", "prod"}:
            env = "dev"

        return cast(Literal["dev", "prev", "prod"], env)


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

        return {**base_config, **env_config}
