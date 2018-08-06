import nltk
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer

# experiment with chunking (grouping words into hopefully meaningful chunks). One of main goals is ot group into noun phrases (one or more words that contain a noun, maybe some descriptive words, mybe a verb, and maybe something like an adverb). The idea is to group nouns with the words that are in relation to them

# + = match 1 or more
# ? = match 0 or 1 repetition
# * = match 0 or more repetitions
# . = any character except a new line

# the POS tags are denoted with < and > and we can also place regular expressions within tags themselves to account for things like "all nouns" (ie <N.*>)

train_text = state_union.raw("2005-GWBush.txt")
sample_text = state_union.raw("2006-GWBush.txt")                                                                    # the following are training and testing data which are the 2005 and 2006 (respectively) state of the union speeches by President George W Bush 

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try: 
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""                                                   # the line here is broken down as follows:
                                                                                                                    # <RB.?>* = 0 or more of any tense of adverb, followed by
                                                                                                                    # <VB.?>* = 0 ore more of any tense of verb, followed by
                                                                                                                    # <NNP>+ = 1 or more proper nouns, followed by
                                                                                                                    # <NN>? = 0 or 1 singular noun
            chunkParser = nltk.RegexpParser(chunkGram)
            chunked = chunkParser.parse(tagged)
            
            print(chunked)
            for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):                                 # iteratte through the subtrees to see the chunks we've declared with the Chunk lable above in the chunkgram variable
                print(subtree)

            chunked.draw()
    except Exception  as e:
        print(str(e))

process_content()
