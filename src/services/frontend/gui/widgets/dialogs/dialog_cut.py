

def cut_text_for_dialogs(text: str, max_length: int) -> str:
    """
        Cut text for pretty output title or text in dialog widget
        :param text: text which need to cut
        :param max_length: max length this text
        :return: text in pretty format
    """
    if '|' in text:
        text = text.split('|')[0].strip()

    if '\n' in text:
        text = text.split('\n')[0].strip()

    if len(text) > max_length:
        text = text[:max_length]

    return text

