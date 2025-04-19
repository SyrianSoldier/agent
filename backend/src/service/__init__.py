from src.service import log_service, db_service,chat_service,serssion_service, flow_service
from src.service.base_service import BaseService


services: list[type[BaseService]] = [
    log_service.LogService,
    db_service.DBService,
    serssion_service.SeesionService,
    chat_service.ChatService,
    flow_service.FlowService
]
