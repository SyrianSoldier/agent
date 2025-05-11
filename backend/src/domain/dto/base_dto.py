from dataclasses import dataclass

@dataclass
class BaseDto():
    pass

@dataclass
class PaginationDto(BaseDto):
    pagesize:int = 10
    pagenum:int = 1
