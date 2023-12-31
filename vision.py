# -*- coding:utf-8 -*-
"""
@Time:    2023/12/15 16:48
@Author:  Evan Wong
@File:    vision.py
@Project: NAOAIGC
@Description: 
"""
import re

import numpy as np

import SparkApi
from data import results
from SparkParam import *


prompt = "想象一下，你正在帮助我与NAO机器人进行交互。" \
         "在任何给定的时间点，你都具备以下能力。你还需要为某些请求输出代码。" \
         "如果请求还指定给出了dictionary: dictName, key: keyName，那么说明该要求请求返回值，你需要将字典对应的键的值修改为需要返回的值。" \
         "Question - 你可以向我提出一个澄清性问题，只要您特别注明 +\"Question+\"即可。" \
         "Code - 输出代码命令，实现预期目标。" \
         "Reason - 在输出代码后，解释你为什么要这样做" \
         "" \
         "NAO机器人所在的环境包含一个NAO机器人和若干物体。除NAO机器人外，其他物体均不可移动。" \
         "你能够使用代码中的视觉控制模块中的方法，完成给定的任务，请勿使用任何其他假设函数：" \
         "（1）recognize(): 调用该方法，机器人将识别眼前的物体，并返回一个字符串作为识别的结果。" \
         "" \
         "下面给出一个示例：" \
         "我：可乐的位置在哪？dictionary: results, key: coke_position" \
         "你：Code - " \
         "```python" \
         "results['coke_position'] = getPosition('coke')" \
         "```" \
         "" \
         "再次强调你的任务是生成解决任务的代码。" \
         "并且你的所有回答应该精要简短，尤其是当涉及到代码的时候。" \
         "请注意不要使用未给出的函数！"


text = []


def find_code_and_execute(s):
    # 使用正则表达式找到代码块
    code = re.findall(r'```python(.*?)```', s, re.DOTALL)

    # 如果找到了代码块
    if code:
        # 执行每一个代码块
        for block in code:
            exec(block.strip())


def recognize():
    return "wyr"


def getPosition(item):
    return [0.95, -0.9, np.pi/2]


def visionControl(task, key='', nao=None):
    Input = prompt + "接下来是我的指令，请完成你的任务，注意不要使用我未给出的函数，" \
                     "如果请求还指定给出了dictionary: dictName, key: keyName，" \
                     "那么说明该要求请求返回值，你需要将字典对应的键的值修改为需要返回的值：" + task
    if key:
        Input += "dictionary: results, "
        Input += "key: " + key
    question = check_len(get_text("user", Input, text))
    SparkApi.answer = ""
    print("visionControl:\n星火:", end="")
    SparkApi.main(app_id, api_key, api_secret, Spark_url3, domain3, question)
    get_text("assistant", SparkApi.answer, text)
    find_code_and_execute(SparkApi.answer)

