def fetch(settings, format_lines, get_rows, get_cols):
    import requests
    coins = [s.strip() for s in settings.get('crypto_list', '').split(',') if s.strip()]
    if not coins:
        return [format_lines('CRYPTO', 'NO COINS', 'CONFIGURE')]
    currency = settings.get('currency_symbol', '$').strip() or '$'
    try:
        r = requests.get(
            'https://api.coingecko.com/api/v3/simple/price',
            params={'ids': ','.join(coins), 'vs_currencies': 'usd', 'include_24hr_change': 'true'},
            timeout=10
        ).json()
    except Exception:
        return [format_lines('CRYPTO', 'ERROR', 'API FAIL')]
    rows = get_rows()
    pages = []
    for i in range(0, len(coins), rows):
        chunk = coins[i:i+rows]
        price_lines, change_lines = [], []
        for c in chunk:
            d = r.get(c, {})
            price = d.get('usd')
            chg = d.get('usd_24h_change')
            sym = c[:5].upper()
            if price is not None:
                price_lines.append(f'{sym} {currency}{price:,.0f}' if price >= 1 else f'{sym} {currency}{price:.4f}')
                icon = '🟩' if (chg or 0) >= 0 else '🟥'
                change_lines.append(f'{sym} {icon}{chg:+.1f}%' if chg is not None else f'{sym} N/A')
            else:
                price_lines.append(f'{sym} ERR')
                change_lines.append(f'{sym} ERR')
        pad = [''] * (rows - len(chunk))
        pages.append(format_lines(*(price_lines + pad)))
        pages.append(format_lines(*(change_lines + pad)))
    return pages or [format_lines('CRYPTO', 'NO DATA', '')]
