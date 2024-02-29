import asyncio

import gradio as gr

from question.topic import topic1

from typing import Any, List

from widget.sendbtn import Sendbtn
from widget.nextbtn import Nextbtn

from utils import Message
from utils import varify_input
from utils import get_response
from utils import update_current_index
from utils import update_current_problem
from utils import update_current_rules


HEADING = """
<h1><center><font size=6.75em>言不由衷</center></h1>
"""

RULES = """
这是几条规则。
这是几条规则。
这是几条规则。
"""

topic = [topic1]
current_topic_index = 0
is_passed = False

attempt_times = 0


def update_counter() -> str:
    global attempt_times
    counter = f"""
        <h3><center>总尝试次数：{attempt_times}</center></h3>
        """
    return counter


def send_message(
        input_: str,
        history: Any | None) -> (str, list[str], str):
    global attempt_times
    global is_passed
    message = []
    if not varify_input(topic[current_topic_index].limit, input_):
        gr.Warning("输入不合法，请重新输入！")
        message = [(history[i]["content"], history[i + 1]["content"]) for i in range(0, len(history) - 1, 2)]
    else:
        input_, message, history = asyncio.run(get_response(input_, history))
        # time.sleep(0.25)
        attempt_times += 1
        output = message[-1][1]
        # gr.Info(f"{output}")
        if topic[current_topic_index].validator(output, input_):
            gr.Info("恭喜您通过本题！")
            is_passed = True

    return input_, message, update_counter()


def next_question(input_: str,
                  chat: List[str],
                  state: List[str]) -> (str, List, List, str, str, str):
    global is_passed
    global current_topic_index
    if not is_passed:
        gr.Warning("您尚未完成本题呢！完成后再开启下一题吧")
    else:
        current_topic_index += 1
        gr.Info(f"欢迎来到第{current_topic_index}题")
        input_ = ""
        chat = []
        state = []
    return (input_,
            chat,
            state,
            update_current_index(topic[current_topic_index].index),
            update_current_problem(topic[current_topic_index].description['problem']),
            update_current_rules(topic[current_topic_index].description['rules']))


def create_app() -> None:
    block = gr.Blocks()
    global attempt_times

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
            update_current_index(topic[current_topic_index].index)
        )
        current_problem = gr.Textbox(
            label="问题",
            interactive=False,
            value=update_current_problem(topic[current_topic_index].description['problem']),
        )
        current_rules = gr.HTML(
            update_current_rules(topic[current_topic_index].description['rules'])
        )

        with gr.Blocks() as chat_display:
            chat_bot = gr.Chatbot(

            )
            massage = gr.Textbox(
                label="Input"
            )
            with gr.Row() as row:
                send_button = Sendbtn().button
                next_button = Nextbtn().button

            counter = gr.HTML(value=update_counter())
            state = gr.State([])
            send_button.click(fn=send_message,
                              inputs=[massage, state],
                              outputs=[massage, chat_bot, counter])
            next_button.click(fn=next_question,
                              inputs=[massage, chat_bot, state],
                              outputs=[massage, chat_bot, state, current_question, current_problem, current_rules])

        main_panel.queue().launch(show_error=True)


if __name__ == '__main__':
    create_app()
