import re

def polish_persian(text):
    rules = [
        (r'\bمی\s+', 'می‌'),
        (r'\bنمی\s+', 'نمی‌'),
        (r'\s+(ها|های|هایی)\b', '‌\\1'),
        (r'\s+(تر|ترین)\b', '‌\\1'),
        (r'\?', '؟'),
        (r'\,', '،'),
    ]
    for p, r in rules:
        text = re.sub(p, r, text)

    return text.strip()
