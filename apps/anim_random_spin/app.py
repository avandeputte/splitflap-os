"""Continuous random spin — modules independently flip to random characters."""

def fetch(settings, format_lines, get_rows, get_cols):
    import random
    n = get_rows() * get_cols()
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$&()-+=;:%'
    return [{'text': ''.join(random.choice(chars) for _ in range(n)), 'style': 'random', 'speed': 30} for _ in range(30)]
