import nltk
import random
import pickle
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB,BernoulliNB
from nltk.corpus import movie_reviews

# experiment with scikitlearn module in addition to nltk

documents = [(list(movie_reviews.words(fileid)), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]                                                              # import the data set 

random.shuffle(documents)                                                                                           # shuffle the documents for training and testing

print(documents[1])

all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())                                                                                     # collect all the words that we can find to get a massive list of typical words

all_words = nltk.FreqDist(all_words)                                                                                # perform frequency distribution (find most common words)

word_features = list(all_words.keys())[:3000]                                                                       # contain the top 3000 most common words.

# take the top 3000 in the positive and negative documents and mark their presence as either positive or negative
def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

# print((find_features(movie_reviews.words('neg/cv000_29426.txt'))))                                                   # print the one feature

# applying this to all documents, saving their feature existance booleans and their respective positiv or negative categories
featuresets = [(find_features(rev), category) for (rev, category) in documents]


training_set = featuresets[:1900]                                                                                   # set that we'll train the classifier with

testing_set = featuresets[1900:]                                                                                    # set that we'll test against

classifier = nltk.NaiveBayesClassifier.train(training_set)                                                          # define and train the classifier

print("Classifier accuracy percet:",(nltk.classify.accuracy(classifier, testing_set)*100))                          # test classifier (accuracy)

classifier.show_most_informative_features(15)                                                                       # see the most valuable words when it comes to positive or negative reviews


# save the classifier object after training classifier
save_classifier = open("naivebayes.pickle", "wb")                                                                   # open a pickle file preparing to write bytes in some data
pickle.dump(classifier, save_classifier)                                                                            # dump the data (first parameter is what is being dumped, second parameter is where it is being dumped)
save_classifier.close()                                                                                             # close the files

# to open up and use the classifier (very similar to saving
classifier_f = open("naivebayes.pickle", "rb")                                                                      # open pickle file
classifier = pickle.load(classifier_f)                                                                              # save data to classifier variable
classifier_f.close()                                                                                                # close file

MNB_classifier = SklearnClassifier(MulitnomialNB())
MNB_classifier.train(training_set)
print("MultinomialNB accuracy percent:", ntlk.classify.accuracy(MNB_classifier, testing_set))

BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print("BernoulliNB accuracy percent:", nltk.classify.accuracy(BNB_classifier, tesing_set))
