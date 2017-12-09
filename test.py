from __future__ import unicode_literals

from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import arabic_reshaper
from wordcloud import WordCloud

text = u"انا احب اللغة العربية و حروفها I love English words"
reshaped_text = arabic_reshaper.reshape(text)
plt.title('Développés et fabriqués')
plt.xlabel("réactivité nous permettent d'être sélectionnés et adoptés")
plt.ylabel('André was here!')
plt.text(0.2, 0.8, 'Institut für Festkörperphysik', rotation=45)
plt.text(0.2, 0.8, reshaped_text, rotation=38)
plt.text(0.4, 0.2, 'AVA (check kerning)')

plt.show()
