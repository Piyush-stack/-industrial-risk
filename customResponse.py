from mimetypes import init
import pickle
import pandas as pd

import nltk
import inflect
import contractions
from bs4 import BeautifulSoup
import re, string, unicodedata
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

MODEL_FILE_ROOT = "/deploy/models"

def load_model(modelFileName):
  pkl = open(MODEL_FILE_ROOT+'/'+modelFileName, 'rb')
  model = pickle.load(pkl) 
  print("Loading: "+str(type(model)))
  pkl.close()
  return model

tfidfvectorizer = load_model('tfIdfModel.pkl')
le = load_model('labelEncoder.pkl')
clf = load_model('customResponseClassifier.pkl')
responses = load_model('responses.pkl')

# Pipeline for text cleaning

def denoise_text(text):
    # Strip html if any. For ex. removing <html>, <p> tags
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    # Replace contractions in the text. For ex. didn't -> did not
    text = contractions.fix(text)
    return text

def tokenize(text):
    return nltk.word_tokenize(text)

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words
def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words
def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words
def replace_numbers(words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words
def remove_numbers(words):
    """Remove all integer occurrences in list of tokenized words with textual representation"""
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = ''
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words
def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words
def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas.append(lemma)
    return lemmas

def normalize_text(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    #words = remove_numbers(words)
    #words = remove_stopwords(words)
    #words = stem_words(words)
    words = lemmatize_verbs(words)
    return words

def text_clean(text):
    text = denoise_text(text)
    text = ' '.join([x for x in normalize_text(tokenize(text))])
    return text

def preprocess_input(text):
  text = text_clean(text)
  text_vectors = tfidfvectorizer.transform([text])
  text_vectors.toarray()
  text_vectors = pd.DataFrame(text_vectors.todense(), columns = tfidfvectorizer.get_feature_names())
  return text_vectors

def get_tag(text):
  text_vectors = preprocess_input(text)
  prediction = clf.predict(text_vectors)
  tag = le.inverse_transform(prediction)
  return tag[0]

def manual_corrections(text):
  if text.lower() == "bye":
    return "Exit", True
  elif text.lower() == "hi" or text.lower() == "hello":
    return "Intro",True
  else:
    return "",False

def get_response_for_tag(tag):
  if tag.lower() in responses.keys():
    return responses[tag.lower()]
  else:
    return "Can you please rephrase that perhaps?"

def ask_bot(text):
  tag = get_tag(text)
  tag_manual, override = manual_corrections(text)
  if override:
    tag = tag_manual
  response = get_response_for_tag(tag)
  return response

if __name__ == "__main__":
    print("Testing sample!!")
    response = ask_bot("Hi, How are you?")
    print("User : Hi, How are you?")
    print("Bot: "+str(response))


