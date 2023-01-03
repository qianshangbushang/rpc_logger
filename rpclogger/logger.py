#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :logger.py.py
# @Time      :2022/12/26 11:43
import os.path
import sys
import traceback

import requests
import yaml


def load_logger_conf():
    conf_path = "./framework.yaml"
    if not os.path.exists(conf_path):
        return []
    with open(conf_path, "r") as f:
        conf = yaml.safe_load(f)
    return conf.get("logger", [])


def init_logger():
    from loguru import logger
    logger_conf = load_logger_conf()
    # 限定类型必须数组类型, 否则使用默认logger
    if not isinstance(logger_conf, list):
        return logger

    for c in logger_conf:
        add_handler(logger, c)
    return logger


def add_handler(logger, conf: dict):
    logger_type = conf.get("logger_type", "")
    if logger_type == "console":
        logger.add(sys.stdout, **conf)

    if logger_type == "file":
        add_file_logger(logger, conf)

    if logger_type == "rpc":
        add_rpc_logger(logger, conf)
    return


"""
    file_path: ""        # 日志文件路径
    rotation: "12:00"    # 滚动周期： 1 week, 1 day, 10 MB
    retention: "10 days" # 保存时长
    compression: "zip"   # 文件压缩格式
    enqueue: true        # 日志先进队列，防止多线程或者多进程不安全
    serialize: false     # 是否json序列化
    format: “{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}” # 格式，仅对本地日志生效
    
"""


def add_file_logger(logger, conf: dict):
    file_path = conf.get("file_path", "./log/rpc.log")
    logger.add(file_path, )
    return


def add_rpc_logger(logger, conf: dict):
    rpc_sink = create_rpc_sink(conf)
    logger.add(rpc_sink, serialize=False)
    return


def create_rpc_sink(conf: dict):
    def rpc_sink(message):
        record = message.record
        data = {
            "file_name": record["file"].name,
            "file_path": record["file"].path,
            "function": record["function"],
            "level": record["level"].name,
            "line_no": record["line"],
            "message": record["message"],
            "time": record["time"].strftime("%Y%m%d"),
            "process": str(record["process"].id),
            "thread": str(record["thread"].id)
        }
        addr = conf["target"].split("://")[1]
        proto = conf["proto"]
        try:
            requests.post(
                url=f"{proto}://{addr}/china_life.proto_repo.rpc_logger.rpc_logger/PushRecord",
                json=data,
                headers={
                    'content-type': "application/json"
                },
                timeout=(1, 1)
            )
        except Exception as e:
            traceback.print_exc()
            raise Exception("remote server not found")
        return

    return rpc_sink


logger = init_logger()
