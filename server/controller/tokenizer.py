import re

def title_tokenizer(title):
    '''given title, return tokenized tags'''
    # naive split for now
    return clean_whitespace(title).split(' ')

def get_insensitive_unique(*args):
    '''given N lists, return the case insensitive unique list'''
    unique = {}

    for array in args:
        assert isinstance(array, (list, tuple)), 'function requires list or tuple'
        unique.update({val.lower(): val for val in array})

    return list(unique.values())

def clean_whitespace(value):
    return re.sub(r's+', ' ', value.strip())
