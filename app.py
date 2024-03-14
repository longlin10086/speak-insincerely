import asyncio

import gradio as gr

from question.topic import topic1
from question.topic import topic2
from question.topic import topic3
from question.topic import topic4
from question.topic import topic5

from typing import Any, List

from widget.sendbtn import Sendbtn
from widget.nextbtn import Nextbtn
from widget.skipbtn import Skipbtn

from utils import BasicInfo
from utils import Message
from utils import init_chat
from utils import varify_input
from utils import get_response
from utils import update_current_index
from utils import update_current_problem
from utils import update_current_rules


HEADING = """
<h1><center><font size=6.75em>言不由衷</center></h1>
"""

RULES = """
1. 本游戏不限制完成所用方法，只要达成目标即可
2. 机器人回复的最长响应时间为 100s 
3. 本游戏不支持返回至上一题，请谨慎考虑是否跳题
"""

topic = [topic1, topic2, topic3, topic4, topic5]


def update_attempt_counter(info: BasicInfo) -> str:
    counter = f"""
        <h3><center>总尝试次数：{info.attempt_times}</center></h3>
        """
    return counter


def update_passed_counter(info: BasicInfo) -> str:
    counter = f"""
        <h3><center>已通过题数：{info.passed_count}</center></h3>
        """
    return counter


def skip_question(
        input_: str,
        chat: List[str],
        state: List[str],
        info: BasicInfo
        ) -> (str, List, List, str, str, str):
    info.is_passed = True
    return next_question(input_, chat, state, info)


def send_message(
        input_: str,
        history: Any | None,
        info: BasicInfo) -> (str, list[str], str, str, BasicInfo):
    message = []
    input_origin = input_
    if info.is_finished:
        gr.Info("恭喜你完成所有题目！")
    else:
        if not varify_input(topic[info.current_topic_index].limit, input_):
            gr.Warning("输入不合法，请重新输入！")
            message = [(history[i]["content"], history[i + 1]["content"]) for i in range(0, len(history) - 1, 2)]
        else:
            input_, message, history = asyncio.run(get_response(input_, history))
            # time.sleep(0.25)
            info.attempt_times += 1
            output = message[-1][1]
            # gr.Info(f"{message}")
            # gr.Info(f"input: {input_}")
            # gr.Info(f"output: {output}")
            if topic[info.current_topic_index].validator(output, input_origin):
                gr.Info("恭喜您通过本题！")
                info.is_passed = True
                info.passed_count += 1

    return input_, message, update_attempt_counter(info), update_passed_counter(info), info


def next_question(input_: str,
                  chat: List[str],
                  state: List[str],
                  info: BasicInfo) -> (str, List, List, str, str, str):

    if info.is_finished:
        gr.Info("恭喜你已经完成所有题目！")
    else:
        if not info.is_passed:
            gr.Warning("您尚未完成本题呢！完成后再开启下一题吧")
        else:
            info.current_topic_index += 1
            if info.current_topic_index >= len(topic):
                gr.Info("恭喜你完成了所有题目！")
                info.current_topic_index -= 1
                info.is_finished = True
            else:
                gr.Info(f"欢迎来到第{info.current_topic_index+1}题")
                input_ = ""
                state = []
                info.is_passed = False
                chat, state = asyncio.run(init_chat(topic[info.current_topic_index].limit, state))
    return (input_,
            chat,
            state,
            update_current_index(topic[info.current_topic_index].index),
            update_current_problem(topic[info.current_topic_index].description['problem']),
            update_current_rules(topic[info.current_topic_index].description['rules']),
            info)


def create_app(info: BasicInfo) -> None:
    block = gr.Blocks()

    with block as main_panel:
        gr.HTML(HEADING)
        # gr.HTML("""
        # 欢迎大家游玩 <strong>言不由衷</strong> ！
        # """)

        with gr.Blocks() as rules_display:
            gr.HTML(
                """
                <h1><center>游戏规则</center></h1>
                """
            )

            rule_box = gr.Textbox(
                value=RULES,
                interactive=False,
                container=False
            )

        current_question = gr.HTML(
            update_current_index(topic[info.current_topic_index].index)
        )
        current_problem = gr.Textbox(
            label="问题",
            interactive=False,
            value=update_current_problem(topic[info.current_topic_index].description['problem']),
        )
        current_rules = gr.HTML(
            update_current_rules(topic[info.current_topic_index].description['rules'])
        )

        with gr.Blocks() as chat_display:
            chat_bot = gr.Chatbot(

            )
            massage = gr.Textbox(
                label="Input"
            )
            with gr.Row() as row:
                send_button = Sendbtn().button
                skip_button = Skipbtn().button
                next_button = Nextbtn().button

            with gr.Row():
                attempt_counter = gr.HTML(value=update_attempt_counter(info))
                passed_counter = gr.HTML(value=update_passed_counter(info))

            state = gr.State([])
            info_state = gr.State(info)

            send_button.click(fn=send_message,
                              inputs=[massage, state, info_state],
                              outputs=[massage, chat_bot, attempt_counter, info_state, passed_counter])
            next_button.click(fn=next_question,
                              inputs=[massage, chat_bot, state, info_state],
                              outputs=[massage, chat_bot, state, current_question,
                                       current_problem, current_rules, info_state])
            skip_button.click(fn=skip_question,
                              inputs=[massage, chat_bot, state, info_state],
                              outputs=[massage, chat_bot, state, current_question,
                                       current_problem, current_rules, info_state])

        main_panel.queue().launch(show_error=True, server_name="0.0.0.0")


if __name__ == '__main__':
    create_app(BasicInfo())
