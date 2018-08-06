from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# play around with stopWords (Words that we may find useless like "Umm" or "Uh") and remove them from the text

example_sent = "This is a sample sentence, showing off the stop words filtration."                                  # sample sentence to be tokenized

stop_words = set(stopwords.words('english'))                                                                        # stop_words now holds the set of all stopwords that already come in ntlk in addition to the added stopword 'english'

word_tokens = word_tokenize(example_sent)                                                                           # tokenize the sample sentence into words

filtered_sentence = [W for W in word_tokens if not W in stop_words]                                                 # filtered_sentence holds the list of all words tokenized if a word is not a stopword

filtered_sentence = []

for W in word_tokens:                                                                                               # go through each word in the word tokenization of the sentence
    if W not in stop_words:                                                                                         # if a word is not a stopword, append that word to the filtered sentence list
        filtered_sentence.append(W)

print(word_tokens)                                                                                                  # print out the word tokenizaton of the sentence
print(filtered_sentence)                                                                                            # print out the filtered sentence 
