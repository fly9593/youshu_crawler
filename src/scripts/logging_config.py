import logging
import logging.config
import os
import threading
from datetime import datetime

from scripts.config import Config

thread_local = threading.local()


# def setup_logging():
#     """Setup logging configuration"""
#     log_filename = f"app_log_{datetime.now().strftime('%Y-%m-%d')}.log"
#
#     logging_config = {
#         "version": 1,
#         "disable_existing_loggers": False,
#         "formatters": {
#             "standard": {
#                 "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
#             }
#         },
#         "handlers": {
#             "file_handler": {
#                 "class": "logging.FileHandler",
#                 "formatter": "standard",
#                 "level": "INFO",
#                 "filename": log_filename,
#                 "mode": "a"
#             }
#         },
#         "loggers": {
#             "": {
#                 "handlers": ["file_handler"],
#                 "level": "INFO",
#                 "propagate": True
#             }
#         }
#     }
#
#     logging.config.dictConfig(logging_config)

# def setup_logging():
#     conf = Config()
#     project_dir = conf.project_dir
#     log_dir = os.path.join(project_dir, "logs")
#     # 确保日志目录存在
#     # log_dir = 'src/logs'
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#     # log_filename = datetime.now().strftime("youshu_log_%Y-%m-%d_%H-%M-%S.log")
#     log_filename = os.path.join(log_dir, datetime.now().strftime("youshu_log_%Y-%m-%d_%H-%M-%S.log"))
#
#     logging.config.dictConfig({
#         'version': 1,
#         'disable_existing_loggers': False,
#         'formatters': {
#             'default': {
#                 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             },
#         },
#         'handlers': {
#             'file': {
#                 'class': 'logging.FileHandler',
#                 'filename': log_filename,
#                 'formatter': 'default',
#                 'encoding': 'utf-8',
#             },
#             'console': {
#                 'class': 'logging.StreamHandler',
#                 'formatter': 'default',
#             },
#         },
#         'root': {
#             'handlers': ['file', 'console'],
#             'level': 'INFO',
#         },
#     })


def setup_logging(start_page, end_page):
    conf = Config()
    project_dir = conf.project_dir
    log_dir = os.path.join(project_dir, "logs")
    # 确保日志目录存在
    # log_dir = 'src/logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置日志文件名
    log_filename = os.path.join(
        log_dir,
        f"youshu_log_{datetime.now().strftime('%Y%m%d%H%M%S')}_{start_page}_{end_page}.log"
    )

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_filename,
                'formatter': 'default',
                'encoding': 'utf-8',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
    })


def setup_logging_threading(start_page, end_page, thread_id):
    # thread_local.logger_initialized = True
    conf = Config()
    project_dir = conf.project_dir
    log_dir = os.path.join(project_dir, "logs")
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 设置日志文件名，包括线程 ID
    log_filename = os.path.join(
        log_dir,
        f"youshu_log_{datetime.now().strftime('%Y%m%d%H%M%S')}_{start_page}_{end_page}_{thread_id}.log"
    )

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
        },
        'handlers': {
            'file': {
                'class': 'logging.FileHandler',
                'filename': log_filename,
                'formatter': 'default',
                'encoding': 'utf-8',
            },
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
            },
        },
        'root': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
        },
    })


# 在项目启动时调用
# setup_logging()

# def setup_logging():
#     # 获取当前时间，精确到秒
#     current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
#     log_filename = f'my_log_{current_time}.log'
#
#     # 创建 logger 对象
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)  # 设置全局日志级别
#
#     # 创建日志目录（如果不存在）
#     log_dir = 'logs'
#     if not os.path.exists(log_dir):
#         os.makedirs(log_dir)
#
#     # 创建文件处理器并设置级别为 INFO
#     file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
#     file_handler.setLevel(logging.INFO)
#
#     # 创建控制台处理器并设置级别为 INFO
#     console_handler = logging.StreamHandler()
#     console_handler.setLevel(logging.INFO)
#
#     # 创建日志格式器
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#
#     # 将格式器添加到处理器
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)
#
#     # 将处理器添加到 logger
#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)
#
#     return logger
