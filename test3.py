from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import arabic_reshaper

reshaped_text = arabic_reshaper.reshape(u'Plus Plus MOIns')
artext = get_display(reshaped_text)

plt.text(0.25, 0.45, artext, name='Times New Roman', fontsize=50)
plt.show()
