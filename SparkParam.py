# -*- coding:utf-8 -*-
"""
@Time:    2023/12/16 18:52
@Author:  Evan Wong
@File:    SparkParam.py
@Project: NAOAIGC
@Description: 
"""
import re

app_id = "3bae7be3"  # 填写控制台中获取的 APP ID 信息
api_secret = "OTBmZTQ3MWY1YjAwNzkyNDE3YjAzZGEy"  # 填写控制台中获取的 APISecret 信息
api_key = "f66463dd1ed3095d4c22f87d624d431c"  # 填写控制台中获取的 APIKey 信息

domain15 = "general"  # v1.5版本
domain2 = "generalv2"  # v2.0版本
domain3 = "generalv3"  # v2.0版本

Spark_url15 = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url2 = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
Spark_url3 = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址


# length = 0
def get_text(role, content, text):
    jsoncon = {"role": role, "content": content}
    text.append(jsoncon)
    return text


def get_length(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def check_len(text):
    while get_length(text) > 8000:
        del text[0]
    return text
