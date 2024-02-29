import asyncio

import gradio as gr

from question.topic import topic_type
from question.topic import topic1

from typing import Any

from widget.sendbtn import Sendbtn
from widget.nextbtn import Nextbtn

from utils import Message
from utils import varify_input
from utils import get_response


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
        output = message[-1]
        if topic[current_topic_index].validator(output, input_):
            gr.Info("恭喜您通过本题！")
            is_passed = True

    return input_, message, update_counter()


def display_question(topic_: topic_type) -> type(gr.Blocks):
    with gr.Blocks() as questions_display:
        current_question = gr.HTML(
            f"""
            <h2><center>第 {topic_.index} 题 / 共 10 题</center></h2>
            """
        )
        gr.Textbox(
            label="问题",
            interactive=False,
            value=f'{topic_.description['problem']}',
        )
        gr.HTML(
            f"""
            <h3><font size=4.75rem>要求</h3>
            <p><font size=3.5rem>{"<br>".join(topic_.description['rules'])}</p>
            """
        )
    return questions_display


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

        display_question(topic[current_topic_index])

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
            send_button.click(fn=send_message, inputs=[massage, state], outputs=[massage, chat_bot, counter])

        main_panel.queue().launch(show_error=True)


if __name__ == '__main__':
    create_app()
