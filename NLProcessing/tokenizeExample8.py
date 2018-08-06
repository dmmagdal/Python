import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

# experiment with chinking, which is very similar to chunking, as a basic way to remove a chunk from a chunk. The chunk data removed is called a chink

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")                                                                    # the following are training and testing data which are the 2005 and 2006 (respectively) state of the union speeches by President George W Bush 

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try: 
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            namedEnt = nltk.ne_chunk(tagged, binary = True)                                                         # the option of binary = True means either something is a named entity or not
                                                                                                                    # play around with setting binary = False
                                                                                                                    # NE types/examples include ORGANIZATION, PERSON, LOCATION, DATE, TIME, MONEY, PERCENT, FACILITY, GPE
            namedEnt.draw()
    except Exception  as e:
        print(str(e))

process_content()
