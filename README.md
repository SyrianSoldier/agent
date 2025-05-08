# Agent

## 开发编辑器

请使用vscode开发以获取所有特性



## 环境安装

###  基本环境

前端:

	- node

后端：

 - python 3.13.3
 - mysql  5.6.15
 - navicat

### 安装依赖

前端：

​	1. 下载依赖，yarn

​	2. 启动： npm run dev

后端：

​	1. 安装虚拟环境 python -m venv .venv

​	2. 激活虚拟环境  .venv\Scripts\activate

​	3. 下载依赖  pip install -r requirements.txt

​	4. 新增 agent 数据库

​	5. python main.py 启动项目  找到-Server started at http://localhost:1080

​	6. 查看数据库表是否自动创建 

## vscode插件依赖

1. Mypy Type Checker
2. Pylance
3. Pylint
4. Python
5. Python Debugger




## TODO List

### 前端需求

| 需求清单         | 需求标签 | 需求级别 | 需求难度 | 预估截止日期    | 需求描述                                 | 是否完成 |
| ------------ | ---- | ---- | ---- | --------- | ------------------------------------ | ---- |
| **前端Vue3改造** | ai聊天 | p0   | ⭐⭐   | 2025-4-12 | 把前端项目改成Vue3+typescript+webpack+vuex的 | √    |
| **Chat静态页面** | ai聊天 | p0   | ⭐    |           |                                      |      |
| **Chat页面**   | ai聊天 | P0   | ⭐⭐   |           | 接入后端接口,完成前后端联调                       |      |

### 后端需求

| 需求清单                    | 需求标签     | 需求级别 | 需求难度 | 预估截止日期 | 需求描述                                     | 是否完成    |
| ----------------------- | -------- | ---- | ---- | ------ | ---------------------------------------- | ------- |
| **`ai`聊天接口**            | ai聊天     | p0   | ⭐⭐⭐⭐ |        |                                          |         |
| \|- 获取所有模型类型的接口         |          |      |      |        | 1. 定义一个模型类型枚举, 返回给前端<br />2. 参考下别人的ai网站有哪些流行的模型类型 |         |
| \|- 对模型配置的CRUD接口        |          |      |      |        | 1. 定义一个模型配置`dataclass`<br />2. 数据库建表, 存储对每一个模型的配置 |         |
| \|- 聊天会话管理              |          |      |      |        | 设计聊天会话表                                  |         |
| \|- 会话的历史消息管理           |          |      |      |        | 设计历史消息管理                                 |         |
| \|- 聊天Node节点开发          |          |      |      |        | 1. 根据选择的模型读取模型配置, 将用户提问透传给大模型<br />2. 支持流式/非流式两种方式 |         |
|                         |          |      |      |        |                                          |         |
| **通用接口返回api**           | 后端架构优化一期 | p0   |      |        |                                          |         |
| \|- CRUD通用返回api         |          |      |      |        |                                          | √       |
| \|- class和`dict`的自动双向映射 |          |      |      |        | 这个api可以<br />1. 接收更新,新增接口的dict, 转换成指定的实体类(可以是dataclass, peewee的模型类) (JSONwirezied可以实现吗)<br />2. return_success时候自动将实体类转成dict<br />3. api就叫做 class_instance_to_dict 和 dict_to_class_instance | **ing** |
| **程序异步化改造**             | 后端架构优化一期 | p0   |      |        |                                          |         |
| \|- web请求异步             |          |      |      |        | 接口改为使用`async`<br />( Tornado 的 `RequestHandler` 从 **5.0 版本**开始原生支持 `async/await` 语法) | √       |
| \|- 数据库异步               |          |      |      |        | 使用`peewee-async`                         | √       |
| \|- 网络异步                |          |      |      |        | 增加`httpx`依赖, 取代`requests`                | √       |
| \|- main函数异步            |          |      |      |        | `asyncio` 运行`main`函数                     | √       |
| \|- 封装pewee异步化`sql` API |          |      |      |        | `async_get_or_none()` `async_execute()` `async_execute()` | √       |
| \|- 文件IO异步              |          |      |      |        | `安装依赖aiofiles`                           | √       |
| \|- 异步日志                |          |      |      |        | 单线程 + 队列实现                               | √       |
|                         |          |      |      |        |                                          |         |
| **日志系统改造**              | 后端架构优化一期 | p2   | ⭐⭐   |        |                                          |         |
|                         |          |      |      |        | 性能日志集成到`baseController`中, 统计每个接口响应时间     |         |
|                         |          |      |      |        | 对`sql api`进行封装, 集成性能日志, 统计`sql`执行时间      |         |
|                         |          |      |      |        | 第三方库的`logger`要集成到logger里<br /><br />`2025-04-06 16:10:20 [DEBUG] asyncio:proactor_events.py:633 - Using proactor: IocpProactor`<br /><br />`2025-04-06 16:10:20 [ERROR] tornado.application:ioloop.py:770 - Exception in callback functools.partial(<function app_started_welcome at 0x00000200FA268AE0>)`<br /><br />这两条应该集成到自己的日志里 |         |
|                         |          |      |      |        |                                          |         |
| **sentry集成前后端日志**       | 后端架构优化二期 | p3   | ⭐⭐⭐⭐ |        |                                          |         |





