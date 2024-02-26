

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



