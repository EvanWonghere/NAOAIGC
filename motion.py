# -*- coding:utf-8 -*-
"""
@Time:    2023/12/14 17:09
@Author:  Evan Wong
@File:    motion.py
@Project: NAOAIGC
@Description: 
"""


import SparkApi
import numpy as np

# 以下密钥信息从控制台获取
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
         "你能够使用代码中的动作控制模块中的方法，完成给定的任务，请勿使用任何其他假设函数：" \
         "（1）moveTo(x, y, angle): 输入目标地点的相对于NAO机器人的x, y坐标和旋转角度angle这三个浮点数，机器人就会行走指该位置并旋转指定角度。" \
         "（2）moveToWIthSpeed(x, y, angle, fraction): 输入目标地点的相对于NAO机器人的x, y坐标，旋转角度angle和" \
         "行走速率（0 -- 1.0）这四个浮点数，让机器人以指定速度行走至指定地点并旋转指定角度。" \
         "（3）adjustAndGrab()：调用此函数，机器人将会微调自己的位置，并尝试抓取眼前的物品。" \
         "（4）waveHands()：调用此函数，机器人将会开始挥手。" \
         "" \
         "下面是一个示例场景，说明你该怎么做。假设场景中有两个红色球体：" \
         "我: 走到最远的红球那里去，他的位置信息是[x, y, angle]。" \
         "你: Code - \n" \
         "```python\n" \
         "moveTo(x, y, angle)" \
         "```" \
         "注意如果给定的位置信息是空，你应该给出提醒。" \
         "" \
         "你还可以访问一个 Python 字典，字典的键是对象名称，值是每个对象的 X、Y、angle坐标：" \
         "dict_of_objects = {" \
         "'origin': [0.0, 0.0, 0], " \
         "'mirror': [1.25, -0.15, 0], " \
         "'chair 1': [0.9, 1.15, np.pi/2], " \
         "'orchid': [0.9, 1.65, np.pi/2], " \
         "'lamp': [1.6, 0.9, np.pi/2], " \
         "'baby ducks': [0.1, 0.8, np.pi/2], " \
         "'sanitizer wipes': [-0.3, 1.75, 0], " \
         "'coconut water': [-0.6, 0.0, -np.pi], " \
         "'shelf': [0.95, -0.9, np.pi/2], " \
         "'diet coke can': [1.0, -0.9, np.pi/2], " \
         "'regular coke can': [1.3, -0.9, np.pi/2]}" \
         "" \
         "你准备好了吗？你是否清楚且明白？只需要回答是或否。" \
         "再次强调你的任务是生成解决任务的代码。" \
         "并且你的所有回答应该精要简短，尤其是当涉及到代码的时候。" \


dict_of_objects = {
         'origin': [0.0, 0.0, 0],
         'mirror': [1.25, -0.15, 0],
         'chair 1': [0.9, 1.15, np.pi/2],
         'orchid': [0.9, 1.65, np.pi/2],
         'lamp': [1.6, 0.9, np.pi/2],
         'baby ducks': [0.1, 0.8, np.pi/2],
         'sanitizer wipes': [-0.3, 1.75, 0],
         'coconut water': [-0.6, 0.0, -np.pi],
         'shelf': [0.95, -0.9, np.pi/2],
         'diet coke can': [1.0, -0.9, np.pi/2],
         'regular coke can': [1.3, -0.9, np.pi/2]}


text = []


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


def motionControl(task):
    Input = prompt
    question = check_len(get_text("user", Input))
    SparkApi.answer = ""
    print("星火:", end="")
    SparkApi.main(app_id, api_key, api_secret, Spark_url, domain, question)
    get_text("assistant", SparkApi.answer)

    Input = task
    question = check_len(get_text("user", Input))
    SparkApi.answer = ""
    print("星火:", end="")
    SparkApi.main(app_id, api_key, api_secret, Spark_url, domain, question)
    get_text("assistant", SparkApi.answer)
