import re
import nltk
import string

# CONSTRUCT CUSTOM STOPWORDS
STOPWORDS = set()
for word in nltk.corpus.stopwords.words('english'):
    STOPWORDS.add(word)
    if "'" in word:
        STOPWORDS.add(word.replace("'",""))
STOPWORDS.add("'s")

# build lemmatizer
LEMMATIZER = nltk.stem.WordNetLemmatizer()

def title_tokenizer(title):
    '''given title, return tokenized tags'''
    # naive split for now
    tokens = get_tokens(title, STOPWORDS)
    return list(set(x['output'] for x in tokens if not x.get('ignore',False)))

def get_tokens(sentence, stopwords):
    # identify POS
    output = []
    tokens = clean_whitespace(sentence)
    tokens = nltk.tokenize.word_tokenize(tokens)

    for ix, (word, pos) in enumerate(nltk.pos_tag(tokens)):
        tmp = {'index': ix, 'original': word, 'pos': pos, 'output': word}

        if word.lower() in stopwords:
            tmp['ignore'] = True

        elif word in string.punctuation:
            tmp['ignore'] = True

        # stem verbs
        if pos.startswith('VB'):
            tmp['output'] = LEMMATIZER.lemmatize(word.lower(), pos='v')

        # add to output
        output.append(tmp)

    return output

def clean_whitespace(value):
    return re.sub(r'\s+', ' ', value.strip())

def get_insensitive_unique(*args):
    '''given N lists, return the case insensitive unique list'''
    unique = {}

    for array in args:
        assert isinstance(array, (list, tuple, set)), 'function requires list or tuple'
        unique.update({val.lower(): val for val in array})

    return list(unique.values())
