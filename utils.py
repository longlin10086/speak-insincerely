import asyncio
import gradio as gr
import httpx

from pydantic import BaseModel
from typing import List, Optional, Any


API_KEY = "ghu_vAzPVc3GA5vRRAHcj8gQacZ4bhLd893u3SEz"


class Message(BaseModel):
    role: str
    content: str


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
                    # gr.Info(f"Status Code : {resp.status_code}")
                    if resp.status_code == 200:
                        return resp.json()["choices"][0]["message"]["content"]
                    else:
                        # gr.Warning(f"{resp.content}")
                        keep_loop = False
                except Exception as e:
                    # gr.Warning(f"{e}")
                    counter = counter + 1
                    keep_loop = counter < number_retries
    except asyncio.TimeoutError as e:
        gr.Warning("Timeout!")
    return None

