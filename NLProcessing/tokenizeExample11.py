import nltk
from nltk.corpus import wordnet

# experiment with Wordnet (a lexical database for English language) to find meanings of words, synonyms, antonyms, and more

syns = wordnet.synsets("program")                                                                                   # we're going to use the term program to find sysnsets 
print(syns[0].name())                                                                                               # example of a synset
print(syns[0].lemmas()[0].name())                                                                                   # just the word
print(syns[0].definition())                                                                                         # definition of first synset
print(syns[0].examples())                                                                                           # examples of word use

# to find synonyms of word, use the lemmas. The .antonyms function will find the antonyms of the lemmas
synonyms = []
antonyms = []

for syn in wordnet.synsets("good"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))

# use wordnet to compare the similarity of two words and their tenses
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')

print(w1.wup_similarity(w2))
