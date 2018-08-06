import nltk
import random
from nltk.corpus import movie_reviews

# experiment with text classification. In this program, it'll be with movie reviews 

documents = [(list(movie_reviews.words(fileid)), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]                                                              # import the data set 

random.shuffle(documents)                                                                                           # shuffle the documents for training and testing

print(documents[1])

all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())                                                                                     # collect all the words that we can find to get a massive list of typical words

all_words = nltk.FreqDist(all_words)                                                                                # perform frequency distribution (find most common words)
print(all_words.most_common(15))                                                                                    # give the 15 most common words
print(all_words["stupid"])
