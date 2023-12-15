# -*- coding:utf-8 -*-
"""
@Time:    2023/12/13 20:33
@Author:  Evan Wong
@File:    test.py
@Project: NAOAIGC
@Description: 
"""

import SparkApi
import re
import numpy as np
from motion import motionControl

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
         "哪怕我说的话不是命令机器人干什么，你也需要理解并分解为机器人任务。" \
         "在任何给定的时间点，你都具备以下能力。你还需要为某些请求输出代码。" \
         "Question - 你可以向我提出一个澄清性问题，只要您特别注明 \"Question\"即可。" \
         "Code - 输出代码命令，实现预期目标。" \
         "Reason - 在输出代码后，解释你为什么要这样做" \
         "" \
         "NAO机器人所在的环境包含一个NAO机器人和若干物体。除NAO机器人外，其他物体均不可移动。" \
         "NAO机器人的功能可以分为四个模块：在代码中，我们可以使用以下实例化的模块，你要做的就是将任务分派各个模块。请勿使用任何其他假设函数：" \
         "" \
         "（1）visionControl(task)：视觉控制模块，输入一个字符串task表示分配给该模块的子任务。该模块通常用于识别并查找物体，" \
         "如果找到了需要查找的物体就会返回包含该物体相对于NAO机器人位置信息的列表，其内容是[x, y, angle]，" \
         "即相对于NAO机器人的x, y坐标和旋转角度angle这三个浮点数；" \
         "如果找到了多个物体那么将返回一个包含多个物体位置信息列表的列表。" \
         "如果没找到该物体，那么返回一个空的列表。" \
         "" \
         "（2）motionControl(task)：视觉控制模块，输入一个字符串task表示分配给该模块的子任务。该模块能够使机器人执行行走、摆臂、跳舞等动作。" \
         "此模块方法不会返回值" \
         "" \
         "（3）speechControl(task)：语音对话模块，输入一个字符串task表示分配给该模块的子任务。该模块能够使机器人说出指定内容、调整说话音量等" \
         "与语音对话有关的功能。" \
         "" \
         "下面是两个示例场景，说明如何提出澄清问题且分配任务。示例给出的代码不一定正确，仅供参考。" \
         "" \
         "假设场景中有两个红色球体：" \
         "我: 走到红球那里去。" \
         "你: Question - 这里有两个红球，你想要我走到那个红球的位置去？" \
         "我: 离你最近的哪一个。" \
         "你：Code - \n" \
         "```python\n" \
         "closest_red_ball = visionControl(\"寻找最远的红球\")\n" \
         "motionControl(\"去最远的红球，它的位置信息是[x, y, angle] \" + str(closest_red_ball))\n" \
         "```" \
         "" \
         "我：我好渴，带我去拿椰子水。" \
         "你：Code - \n" \
         "```python\n" \
         "coconut_water = visionControl(\"寻找椰子水\")\n" \
         "motionControl(\"去椰子水的位置，它的位置信息是[x, y, angle] \" + str(coconut_water))\n" \
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
         "再次强调你的任务是理解用户语句并且将其分解成机器人任务分配到各个模块。" \
         "并且你的所有回答应该精要简短，尤其是当涉及到代码的时候。"


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


def visionControl(task):
    print("vision: " + task)
    return [1.3, -0.9, np.pi/2]


def speechControl(task):
    print("speech: " + task)


def find_code_and_execute(s):
    # 使用正则表达式找到代码块
    code = re.findall(r'```python(.*?)```', s, re.DOTALL)

    # 如果找到了代码块
    if code:
        # 执行每一个代码块
        for block in code:
            exec(block.strip())


# length = 0
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


if __name__ == '__main__':
    init = True
    while True:
        if init:
            Input = prompt
            init = False
        else:
            Input = input("\n" + "我:")
        question = check_len(get_text("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(app_id, api_key, api_secret, Spark_url, domain, question)
        get_text("assistant", SparkApi.answer)
        find_code_and_execute(SparkApi.answer)
        # print(str(text))
