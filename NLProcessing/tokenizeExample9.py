import nltk
from nltk.stem import WordNetLemmatizer

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
