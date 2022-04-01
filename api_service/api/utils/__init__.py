def replace_symbol_key_to_stock(dict_symbol):
    dict_symbol["stock"] = dict_symbol.pop("symbol")
    dict_symbol["stock"] = dict_symbol["stock"].lower()
    return dict_symbol
