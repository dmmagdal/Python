import sys
import nltk
from nltk.tokenize import sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import gutenberg

""" for importing files with nltk
if sys.platform.startswith('win'):
    # common locations on Windows
    path += [str(r'C:\nltk_data'),
    os.path.join(sys.prefix, str('nltk_data')),
    os.path.join(sys.prefix, str('lib'), str('nltk_data')),
    os.path.join(os.environ.get(str('APPDATA'), str('C:\\')), str('nltk_data'))]
else:
    # common locations on UNIX and OSX
    path += [
            str('/usr/share/nltk_data'),
            str('/usr/local/share/nltk_data'),
            str('/usr/lib/nltk_data'),
            str('/usr/local/lib/nltk_data')]
"""


# sample text
sample = gutenberg.raw("bible-kjv.txt")

tok = sent_tokenize(sample)

for x in range(5):
    print(tok[x])

"""
# experiment with lemmatizing (operation similar to stemming) which creates actual words rather than non existant ones when stemming

lemmatizer = WordNetLemmatizer()

print(lemmatizer.lemmatize("cats"))
print(lemmatizer.lemmatize("cacti"))
print(lemmatizer.lemmatize("geese"))
print(lemmatizer.lemmatize("rocks"))
print(lemmatizer.lemmatize("python"))
print(lemmatizer.lemmatize("better", pos = "a"))
print(lemmatizer.lemmatize("best", pos = "a"))
print(lemmatizer.lemmatize("run"))
print(lemmatizer.lemmatize("run", 'v'))                                                                             # the only thing to note here is that lemmatize takes a part of speech parameter (if not supplied, default is noun)

"""
