import tornado
from src.controller import chat_controller, base_controller

# 路由表
routes: tornado.routing._RuleList = [
    (r"/", base_controller.BaseController),
    (r"/api/chat", chat_controller.ChatController)
]
