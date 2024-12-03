def split_first_word(series):
    return series.str.split().str[0].to_frame()