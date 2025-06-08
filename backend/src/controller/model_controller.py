from .base_controller import BaseController
from src.service.model_service import ModelService
from src.domain.model.model_config import ModeConfigModel

class AvaliableModelList(BaseController):
    async def get(self) -> None:
        model_list = await ModelService.get_model_list()

        self.return_success(model_list)


class Create(BaseController):
    async def post(self) -> None:
        model_config = self.request_body_to_dto(ModeConfigModel)
        assert model_config.model_name is not None, "模型名称不能为空"
        await ModelService.create_model_config(model_config)
        self.return_success()


class List(BaseController):
    async def get(self) -> None:
        model_config = self.request_body_to_dto(ModeConfigModel)
        total, model_list = await ModelService.get_model_config_list(model_config.model_name, model_config.status)
        self.return_success(model_list) # TODO: 返回一个total + list的dict的时候时候有问题

class Delete(BaseController):
    async def post(self) -> None:
        await ModelService.delete_model(self.body_id)
        self.return_success()


