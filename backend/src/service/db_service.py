from typing_extensions import override, List, Type
from peewee import Model
from src.models.database.base_model import db
from src.models.database.session_model import SessionModel
from .base_service import BaseService

TABLES: List[Type[Model]] = [SessionModel]


class DBService(BaseService):

    @override
    def start(self) -> None:
        self.init_db()

    @override
    def end(self) -> None:
        pass

    def init_db(self) -> None:
        db.connect()
        print("Database connect susccess")
        # safe=True: 有表不创建，没表再创建
        db.create_tables(TABLES, safe=True)
        print("Database table create susccess")
