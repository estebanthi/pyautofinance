def format_symbol_for_ccxt(symbol):
    return symbol.replace("-", "/")


def format_timeframe_for_ccxt(timeframe):
    # We need to invert compression and unit to have a formatted timeframe
    formatted_timeframe = timeframe.value[::-1]
    return formatted_timeframe
