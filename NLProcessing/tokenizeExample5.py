import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

# analyze part of speech (POS) (labeling things as nouns, adjectives, verbs, etc and tense)
# there exists a POS tag list to look at within the nlk documentation

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")                                                                    # the following are training and testing data which are the 2005 and 2006 (respectively) state of the union speeches by President George W Bush 

# now we'll use the Punkt tokenizer and train the tokenizer with the training data 
custom_sent_tokenizer = PunktSentenceTokenizer(train_text)                                                          # train the tokeniser

tokenized = custom_sent_tokenizer.tokenize(sample_text)                                                             # tokenize the sample text

def process_content():                                                                                              # create a new method to run through and tag all POS  per sentence
    try:
        for i in tokenized[:5]:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            print(tagged)
    except Exception as e:
        print(str(e))

process_content()
