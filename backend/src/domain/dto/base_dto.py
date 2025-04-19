import pydantic

class BaseDto(pydantic.BaseModel):
  """接受前端传递的数据,用pydantic做参数校验
  """
