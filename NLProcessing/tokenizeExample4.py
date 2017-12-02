from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# utilize stemming to shorten lookup time and normalize a sentence
# stemming involves taking a sentence that means the same thing (including tense) 

ps = PorterStemmer()

example_words = ["python","pythoner","pythoning","pythoned","pythonly"]                                             # set of words with similar stem

for W in example_words:                                                                                             # go through each word in the stem word set and stem then
    print(ps.stem(W))                                                                                               # print out the result

# now going to practice stemming on a sentence 
new_text = "It is important to be very pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once." # example text to be stemmed using out current stemming list

words = word_tokenize(new_text)                                                                                     # tokenize the sentence into words and store the list in words

for W in words:                                                                                                     # stem all of the words in the set 
    print(ps.stem(W))
