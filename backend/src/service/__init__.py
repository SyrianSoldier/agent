from src.service import chat_serssion_service, log_service, db_service,chat_service,flow_service
from src.service.base_service import BaseService


services: list[type[BaseService]] = [
    log_service.LogService,
    db_service.DBService,
    chat_serssion_service.SeesionService,
    chat_service.ChatService,
    flow_service.FlowService
]
