# -*- coding:utf-8 -*-
"""
@Time:    2023/12/14 17:09
@Author:  Evan Wong
@File:    motion.py
@Project: NAOAIGC
@Description: 
"""


import re

import SparkApi
import numpy as np
from SparkParam import *


prompt = "想象一下，你正在帮助我与NAO机器人进行交互。" \
         "在任何给定的时间点，你都具备以下能力。你还需要为某些请求输出代码。" \
         "Question - 你可以向我提出一个澄清性问题，只要您特别注明 +\"Question+\"即可。" \
         "Code - 输出代码命令，实现预期目标。" \
         "Reason - 在输出代码后，解释你为什么要这样做" \
         "" \
         "NAO机器人所在的环境包含一个NAO机器人和若干物体。除NAO机器人外，其他物体均不可移动。" \
         "你能够使用代码中的动作控制模块中的方法，完成给定的任务，请勿使用任何其他假设函数：" \
         "（1）moveTo(x, y, angle): 输入目标地点的相对于NAO机器人的x, y坐标和旋转角度angle这三个浮点数，机器人就会行走指该位置并旋转指定角度。" \
         "（2）waveHands()：调用此函数，机器人将会开始挥手。" \
         "（3）bow()：调用此函数，机器人将会开始鞠躬动作。" \
         "（4）taichi()：调用此函数，机器人将会开始鞠躬动作。" \
         "" \
         "下面是一个示例场景，说明你该怎么做：" \
         "我: 往前走3m。" \
         "你: Code - \n" \
         "```python\n" \
         "moveTo(3, 0, 0)" \
         "```" \
         "注意如果给定的位置信息是空，你应该给出提醒。" \
         "" \
         "再次强调你的任务是生成解决任务的代码。" \
         "并且你的所有回答应该精要简短，尤其是当涉及到代码的时候。" \
         "请注意不要使用未给出的函数！"


# dict_of_objects = {
#          'origin': [0.0, 0.0, 0],
#          'mirror': [1.25, -0.15, 0],
#          'chair 1': [0.9, 1.15, np.pi/2],
#          'orchid': [0.9, 1.65, np.pi/2],
#          'lamp': [1.6, 0.9, np.pi/2],
#          'baby ducks': [0.1, 0.8, np.pi/2],
#          'sanitizer wipes': [-0.3, 1.75, 0],
#          'coconut water': [-0.6, 0.0, -np.pi],
#          'shelf': [0.95, -0.9, np.pi/2],
#          'diet coke can': [1.0, -0.9, np.pi/2],
#          'regular coke can': [1.3, -0.9, np.pi/2]}


text = []


def find_code_and_execute(s):
    # 使用正则表达式找到代码块
    code = re.findall(r'```python(.*?)```', s, re.DOTALL)

    # 如果找到了代码块
    if code:
        # 执行每一个代码块
        for block in code:
            exec(block.strip())


def motionControl(task, nao=None):
    Input = prompt + "接下来是我的指令，请生成代码完成你的任务，" \
                     "请记住你的任务是让机器人运动，不需要进行别的机器人操作！！！" \
                     "注意不要使用我未给出的函数！！！：" + task
    question = check_len(get_text("user", Input, text))
    SparkApi.answer = ""
    print("motionControl:\n星火:", end="")
    SparkApi.main(app_id, api_key, api_secret, Spark_url3, domain3, question)
    get_text("assistant", SparkApi.answer, text)
    # find_code_and_execute(Spar
