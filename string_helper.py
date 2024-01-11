from ansi_color_codes import Color


def color_string(string: str, color: str) -> str:
    return f"{color}{string}{Color.END}"
