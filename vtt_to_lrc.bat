@echo off
REM 检查是否提供了文件路径
if "%~1"=="" (
    echo 请将VTT文件或文件夹拖放到此BAT文件上。
    pause
    exit /b 1
)

REM 获取BAT文件所在目录
set "SCRIPT_DIR=%~dp0"

REM 设置Python脚本的相对路径
set "PYTHON_SCRIPT=%SCRIPT_DIR%vtt_to_lrc.py"

REM 初始化参数列表
set "PARAMS="

REM 遍历所有拖放的文件或文件夹
:loop
if "%~1"=="" goto :endloop
    set "PARAMS=%PARAMS% "%~1""
    shift
    goto :loop
:endloop

REM 调用Python脚本进行转换
python "%PYTHON_SCRIPT%" %PARAMS%

REM 提示转换完成
echo 转换完成。
pause