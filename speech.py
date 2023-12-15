# -*- coding:utf-8 -*-
"""
@Time:    2023/12/15 16:29
@Author:  Evan Wong
@File:    speech.py
@Project: NAOAIGC
@Description: 
"""
import re

import SparkApi


app_id = "3bae7be3"  # 填写控制台中获取的 APP ID 信息
api_secret = "OTBmZTQ3MWY1YjAwNzkyNDE3YjAzZGEy"  # 填写控制台中获取的 APISecret 信息
api_key = "f66463dd1ed3095d4c22f87d624d431c"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
# domain = "general"  # v1.5版本
domain = "generalv3"    # v2.0版本
# 云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v2.0环境的地址

prompt = "想象一下，你正在帮助我与NAO机器人进行交互。" \
         "在任何给定的时间点，你都具备以下能力。你还需要为某些请求输出代码。" \
         "Question - 你可以向我提出一个澄清性问题，只要您特别注明 +\"Question+\"即可。" \
         "Code - 输出代码命令，实现预期目标。" \
         "Reason - 在输出代码后，解释你为什么要这样做" \
         "" \
         "NAO机器人所在的环境包含一个NAO机器人和若干物体。除NAO机器人外，其他物体均不可移动。" \
         "你能够使用代码中的语言控制模块中的方法，完成给定的任务，请勿使用任何其他假设函数：" \
         "（1）setVolume(fraction): 输入音量的相对大小（0 -- 1.0），输入的浮点数越大NAO机器人的语音音量就越大。" \
         "（2）say(text): 输入一个字符串，NAO机器人就会语音念出该文本。" \
         "" \
         "请注意不要使用未给出的函数！" \


text = []


def find_code_and_execute(s):
    # 使用正则表达式找到代码块
    code = re.findall(r'```python(.*?)```', s, re.DOTALL)

    # 如果找到了代码块
    if code:
        # 执行每一个代码块
        for block in code:
            exec(block.strip())


def setVolume(fraction):
    pass


def say(text):
    print("say: " + text)


def get_text(role, content):
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


def speechControl(task):
    Input = prompt + "接下来是我的指令，请完成你的任务，" \
                     "请记住你的任务是让机器人说话，需要时调整音量大小，不需要进行别的机器人操作！！！" \
                     "注意不要使用我未给出的函数！！！!!!:" + task
    question = check_len(get_text("user", Input))
    SparkApi.answer = ""
    print("SpeechControl:\n星火:", end="")
    SparkApi.main(app_id, api_key, api_secret, Spark_url, domain, question)
    get_text("assistant", SparkApi.answer)
    find_code_and_execute(SparkApi.answer)
