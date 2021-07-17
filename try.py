#import tomopy
#import mkl
#mkl.domain_set_num_threads(1, domain='fft')
import tensorflow as tf
import sqlite3
import numpy as np
import json
import sys
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout 
from tensorflow.keras.optimizers import SGD
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import sklearn
from sklearn.preprocessing import LabelEncoder
import random
import warnings
from tensorflow import keras 
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
warnings.filterwarnings('ignore')

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)
def cleanupSentences(sentence):
    strr=""
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[lemmatizer.lemmatize(word,get_wordnet_pos(word)) for word in sentence_words]
    for i in sentence_words:
        strr=strr+i+" "
    return strr
lemmatizer= WordNetLemmatizer()
intents =json.loads(open('intents.json').read())
words=[]
classes=[]
Y= []
X= []
lettersToBeIgnored=['?','!', ',', '.',':']
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        wordList=nltk.word_tokenize(pattern)
        words.extend(wordList)
        X.append(cleanupSentences(pattern))
        Y.append(intent['tag'])
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
words=[lemmatizer.lemmatize(word,get_wordnet_pos(word)) for word in words if word
 not in lettersToBeIgnored]
words=sorted(set(words))
classes=sorted(set(classes))
enc = LabelEncoder()
enc.fit(Y)
Y = enc.transform(Y)

vocab_size = 10000
embedding_dim = 16
max_len = 20
trunc_type = 'post'
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token) # adding out of vocabulary token
tokenizer.fit_on_texts(X)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(X)
padded = pad_sequences(sequences, truncating=trunc_type, maxlen=max_len)
classes = len(classes)

model = tf.keras.models.Sequential()
model.add(keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(12, activation='relu'))
model.add(keras.layers.Dense(12, activation='relu'))
model.add(keras.layers.Dense(classes, activation='softmax'))
training_labels_final = np.array(Y)
EPOCHS =  500
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(padded, training_labels_final, epochs=EPOCHS,verbose=0)
# print("Hey there!, How can i help you?")
warnings.filterwarnings('ignore')
while True:
       
                string = input(sys.argv[1])
                # string =str(sys.argv[1])
                string=cleanupSentences(string)
    #if string == 'exit': break
                result = model.predict(pad_sequences(tokenizer.texts_to_sequences([string]), truncating=trunc_type, maxlen=max_len))[0]
                result_index=np.argmax(result)
                if result[result_index] > 0.8:
                    category = enc.inverse_transform([np.argmax(result)]) 
                    for i in intents['intents']:
                        if i['tag']==category:
                            print(np.random.choice(i['responses']))
                else:
                        print("Sorry I didn't catch that, could you try again please?")
sys.stdout.flush()
sys.exit(0)
