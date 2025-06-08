import tornado
from src.controller import (
   chat_serssion_controller, model_controller, chat_controller, message_history_controller, model_controller
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
    # 获取所有可用模型列表
    (r"/api/model/avaliable_model/list", model_controller.AvaliableModelList),
    (r"/api/model/create", model_controller.Create),
    (r"/api/model/delete", model_controller.Delete),
    (r"/api/model/list", model_controller.List),

    # 聊天接口
    (r"/api/chat", chat_controller.ChatController),

    # 聊天历史接口
    (r"/api/message_history/create", message_history_controller.Create),
]
