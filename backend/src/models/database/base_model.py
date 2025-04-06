from peewee import MySQLDatabase, Model,SQL,DateTimeField
import datetime
# TODO 把配置信息抽到config目录中
# TODO:添加数据库连接池
# TODO:Redis缓存层
# TODO: 集成Prometheus监控
# TODO: API文档生成（OpenAPI 3.0）使用apistar生成文档
# TODO: 安装peewee-stubs为peewee添加类型提示
db = MySQLDatabase(
    database="agent",
    host="localhost",
    port = 3306,
    user="root",
    password="1234"
)

class BaseModel(Model): # type: ignore[misc]
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP"),SQL('ON UPDATE CURRENT_TIMESTAMP') ])

    class Meta:
        database = db
