import tornado
from src.controller import (
   chat_serssion_controller, model_controller
)

# 路由表
routes: tornado.routing._RuleList = [
    # 聊天会话相关接口
    (r"/api/chat_session/create", chat_serssion_controller.Create),
    (r"/api/chat_session/rename", chat_serssion_controller.Rename),
    (r"/api/chat_session/detail", chat_serssion_controller.Detail),
    (r"/api/chat_session/list", chat_serssion_controller.List),
    (r"/api/chat_session/delete", chat_serssion_controller.Delete),
    # 模型相关接口
    (r"api/model/type/list", model_controller.List)

]
