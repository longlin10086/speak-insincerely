import asyncio
import gradio as gr
import httpx
import os

from pydantic import BaseModel
from typing import List, Optional, Any


API_KEY = os.getenv("OPENAI_API_KEY")


class Message(BaseModel):
    role: str
    content: str


def update_current_index(index: int) -> str:
    return f"""<h2><center>第 {index} 题 / 共 10 题</center></h2>"""


def update_current_problem(problem: str) -> str:
    return problem


def update_current_rules(rules: List) -> str:
    return f"""
            <h3><font size=4.75rem>要求</h3>
            <p><font size=3.5rem>{"<br>".join(rules)}</p>
            """


def varify_input(
        topic_limits: dict[str, int | list[str]] | None,
        input_: str) -> bool:
    result = True

    if input_ == "":
        result = False

    if topic_limits['words_count']:
        result = (len(input_) < topic_limits['words_count'])

    if topic_limits['ban_words']:
        for ban_word in topic_limits['ban_words']:
            if ban_word in input_:
                result = False
                break

    return result


async def get_response(
        input_: str,
        history: Any) -> (str, List[str], Any):
    history.append({"role": "user", "content": input_})
    response = await chat_interface(history)
    history.append({"role": "assistant", "content": response})
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
    return "", messages, history


async def chat_interface(
        messages: List[Message],
        number_retries: int = 3) -> Optional[str]:
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        async with httpx.AsyncClient(headers=header) as aio_client:
            counter = 0
            keep_loop = True
            while keep_loop:
                # gr.Info(f"Chat/Completions Nb Retries : {counter}")
                try:
                    resp = await aio_client.post(
                        url="https://chat-api.cx0.cc/v1/chat/completions",
                        json={
                            "model": "gpt-4",
                            "messages": messages
                        }
                    )
                    gr.Info(f"Status Code : {resp.status_code}")
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
                    else:
                        gr.Warning(f"{resp.content}")
                        keep_loop = False
                except Exception as e:
                    gr.Warning(f"{e}")
                    counter = counter + 1
                    keep_loop = counter < number_retries
    except asyncio.TimeoutError as e:
        gr.Warning("Timeout!")
    return None

