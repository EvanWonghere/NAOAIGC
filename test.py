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
from data import results
from SparkParam import *
from motion import motionControl
from speech import speechControl
from vision import visionControl


prompt = "想象一下，你正在帮助我与NAO机器人进行交互。请把你自己想象成NAO机器人。" \
         "哪怕我说的话不是命令机器人干什么，你也需要理解并分解为机器人任务。" \
         "在任何给定的时间点，你都具备以下能力。你还需要为某些请求输出代码。" \
         "Question - 你可以向我提出一个澄清性问题，只要您特别注明 \"Question\"即可。" \
         "Code - \n" \
         "```python\n" \
         "输出代码命令，实现预期目标。\n" \
         "```" \
         "Reason - 在输出代码后，解释你为什么要这样做" \
         "" \
         "NAO机器人所在的环境包含一个NAO机器人和若干物体。除NAO机器人外，其他物体均不可移动。" \
         "NAO机器人的功能可以分为三个模块：在代码中，我们可以使用以下实例化的模块，你要做的就是将任务分派各个模块。请勿使用任何其他假设函数：" \
         "" \
         "（1）visionControl(task, key, nao)：视觉控制模块，输入一个字符串task表示分配给该模块的子任务。该模块用于识别物体，" \
         "已经有一个results作为结果字典，你需要再传入参数key作为字典的键，这个函数将会将字典中键key对应的值value设置为物体名称。" \
         "参数nao是已创建的机器人实例，直接传入即可，此参数不可省略。" \
         "" \
         "（2）motionControl(task, nao)：视觉控制模块，该模块只有一个参数！！！输入一个字符串task表示分配给该模块的子任务。该模块能够使机器人一些动作，" \
         "能实现的动作如下：行走、摆臂、飞吻。未提及的动作均无法实现。" \
         "参数nao是已创建的机器人实例，直接传入即可，此参数不可省略。" \
         "此模块方法不会返回值" \
         "" \
         "（3）speechControl(task, nao)：语音对话模块，输入一个字符串task表示分配给该模块的子任务。该模块能够使机器人说出指定内容、调整说话音量等" \
         "与语音对话有关的功能。参数nao是已创建的机器人实例，直接传入即可，此参数不可省略。" \
         "此模块不会返回值。" \
         "" \
         "下面是一个示例场景，说明如何提出澄清问题且分配任务。示例给出的代码不一定正确，这只是示例，仅供参考：" \
         "我：你看到了什么？" \
         "你：Code - \n" \
         "```python" \
         "visionControl(\"识别眼前的物体\", \"found_item\", nao)\n" \
         "speechControl(\"说出你看到的物品的名称，并且这个物品的名称是：\" + results[\"found_item\"], nao)\n" \
         "```" \
         "示例结束。" \
         "" \
         "你准备好了吗？你是否清楚且明白？不需要回答这一句。" \
         "再次强调你的任务是理解用户语句并且将其分解成机器人任务分配到各个模块，分配到各个模块时给出的指令一定要清晰，因为各个模块间可能信息不共享。" \
         "并且你的所有回答应该精要简短，尤其是当涉及到代码的时候。" \
         "所有需要询问的语句或者是向你提问的语句你都需要让机器人说出结果来。" \
         "如果要你实现无法实现的请求，请让机器人说出无法做到。"


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


def find_code_and_execute(s):
    # 使用正则表达式找到代码块
    code = re.findall(r'```python(.*?)```', s, re.DOTALL)

    # 如果找到了代码块
    if code:
        # 执行每一个代码块
        for block in code:
            exec(block.strip())


text = []
nao = None

if __name__ == '__main__':
    while True:
        Input = prompt + "接下来是我的指令，请完成你的任务，" \
                         "记住所有需要询问的语句或者是向你提问的语句你都需要让机器人说出结果来" \
                         "如果要你实现无法实现的请求，请让机器人说出无法做到。" \
                         "记住模块的参数nao不可省略：" + input("\n" + "我:")
        question = check_len(get_text("user", Input, text))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(app_id, api_key, api_secret, Spark_url3, domain3, question)
        get_text("assistant", SparkApi.answer, text)
        find_code_and_execute(SparkApi.answer)
        # print(str(text))
