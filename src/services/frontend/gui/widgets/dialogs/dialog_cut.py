

def cut_text_for_dialogs(text: str, 
                         max_length: int,
                         with_first_skip: bool = False) -> str:
    """
        Cut text for pretty output title or text in dialog widget
        :param text: text which need to cut
        :param max_length: max length this text
        :param with_first_skip: skip if first \n is needed
        :return: text in pretty format
    """
    if '|' in text:
        text = text.split('|')[0].strip()

    if '\n' in text:
        if with_first_skip:
            texts = text.split('\n')
            text = texts[0] + '\n' + texts[1].strip()

    if len(text) > max_length:
        text = text[:max_length]

    return text

