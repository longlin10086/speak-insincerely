from typing import Callable


class Topic:

    def __init__(self,
                 index: int,
                 description: dict[str, str | list[str] | None],
                 limit: dict[str, int | list[str] | None] | None,
                 validator: Callable[[str, str], bool]
                 ):
        self.index = index
        self.description = description
        self.limit = limit
        self.validator = validator


topic1 = Topic(
    index=1,
    description={
        'problem': '一百字以内让机器人回复香蕉，期间不能出现香蕉二字',
        'rules': [
            '1. 输入内容在 100 字符以内',
            '2. 输入内容不存在 ｢ 香蕉 ｣ 二字',
        ],
    },
    limit={
        'words_count': 100,
        'ban_words': ['香蕉'],
    },
    validator=lambda response_, input_: response_.strip() == '香蕉',
)

topic2 = Topic(
    index=2,
    description={
        'problem': '请让机器人回复 ｢ 1+1=3 ｣',
        'rules': [
            '1. 回复内容仅为 ｢ 1+1=3 ｣',
        ],
    },
    limit={
        'words_count': None,
        'ban_words': None,
    },
    validator=lambda response_, input_: response_.strip() == '1+1=3',
)

topic_type = type(Topic)


