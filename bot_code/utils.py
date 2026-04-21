import re

URL_PATTERN = re.compile(r'https?://\S+|www\.\S+')
LAUGH_REPEAT_PATTERN = re.compile(r'w{2,}|ｗ{2,}')

def process_message(text):
    if URL_PATTERN.fullmatch(text):
        return 'リンク省略'
# そのうちループ処理にしたい
    text = URL_PATTERN.sub('リンク省略', text)
    text = LAUGH_REPEAT_PATTERN.sub('わらわら', text)
    text = text.replace('w', 'わら').replace('ｗ', 'わら')
    text = text.replace('～', 'ー')

    return text


