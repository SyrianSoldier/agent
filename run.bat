@REM 关闭回显输出
@echo off

@REM 设置utf_8
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

call:help

set /p user_input=请输入命令 : 
if %user_input% equ install call:install 
if %user_input% equ update call:update 
if %user_input% equ dev call:dev_start 
exit /b 

@REM ======================================
@REM 安装依赖
@REM ======================================
:help
echo 📖 帮助信息： 
echo   "install": 下载前后端所有依赖 
echo   "update": 更新所有依赖 
echo   "dev": 启动开发环境 
exit /b 

@REM ======================================
@REM 安装依赖
@REM ======================================
:install_frontend
echo 📦 安装前端依赖... 
cd frontend & yarn install  & echo 📦 前端依赖安装成功...  & cd ..
exit /b

:install_backend
echo 📦 安装后端依赖...
cd backend & call venv/Scripts/activate.bat & pip install -r requirements/dev.txt & echo 📦 后端依赖安装成功... & cd ..
exit /b

:install
call :install_frontend 
call :install_backend 
exit /b

@REM ======================================
@REM 更新依赖
@REM ======================================
:update_frontend
echo 📦 更新前端依赖...
cd frontend & yarn & cd .. & echo 📦 前端依赖更新成功...
exit /b

:update_backend
echo 📦 更新后端依赖...
cd backend & pip install --upgrade -r requirements/dev.txt & cd .. & echo 📦 后端依赖更新成功...
exit /b

:update
call :update_frontend
call :update_backend
exit /b


:dev_start
start "后端" /D backend python main.py 
start "前端" /D frontend yarn run dev
exit /b