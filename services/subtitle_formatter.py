import textwrap

def format_subtitle(text, width=42, max_lines=2):
    wrapped = textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False
    )
    return "\n".join(wrapped[:max_lines])
