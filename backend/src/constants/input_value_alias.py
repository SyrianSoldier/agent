from enum import Enum



class InputValueAlias(Enum):
    USER_QUERY = "$USER_QUERY" # 用户的初始输入
    STATE = "$STATE" # 即在遍历图时的state
