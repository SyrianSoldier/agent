import pydantic
from pydantic import Field
from typing import Annotated

class BaseDto(pydantic.BaseModel):
    """接受前端传递的数据,用pydantic做参数校验"""


class PaginationDto(BaseDto):
    pagesize:  Annotated[int, Field(ge=1)]
    pagenum: Annotated[int, Field(default=10)]
