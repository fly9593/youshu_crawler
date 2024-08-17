@echo off
setlocal

REM 启动第一个main.py实例，传入start_page和end_page参数
start "" python main.py 1 300

REM 启动第二个main.py实例，传入start_page和end_page参数
start "" python main.py 301 600

REM 启动第三个main.py实例，传入start_page和end_page参数
start "" python main.py 601 900

REM 启动第四个main.py实例，传入start_page和end_page参数
start "" python main.py 901 1200

REM 等待所有进程结束
wait

endlocal
