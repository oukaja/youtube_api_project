from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import arabic_reshaper
from wordcloud import WordCloud

text = u"انا احب اللغة العربية و حروفها I love English words"
reshaped_text = arabic_reshaper.reshape(text)
print(reshaped_text)
artext = get_display(reshaped_text)

wordcloud = WordCloud().generate(artext)

