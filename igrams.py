import nltk
from nltk.util import ngrams

text = "Hi How are you? i am fine and you"
token = nltk.word_tokenize(text)
bigrams = ngrams(token, 2)
for gram in bigrams:
    print(gram)
