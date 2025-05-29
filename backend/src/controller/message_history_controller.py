from .base_controller import BaseController
from src.service.message_history_service import MessageHistoryService
from src.domain.model.message_history_model import MessageHistoryModel


class Create(BaseController):
    async def post(self) -> None:
        message_history = self.request_body_to_dto(MessageHistoryModel)

        assert message_history is not None
        assert message_history.content is not None
        assert message_history.session_uuid is not None
        assert message_history.role is not None

        await MessageHistoryService.create_chat_history(message_history)
        self.return_success()

