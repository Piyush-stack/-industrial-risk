# Import libraries
import numpy as np
import os
from flask import Flask, request, jsonify, json
from flask import render_template
import pickle
import dl_predict
import customResponse

MODEL_FILE_ROOT = "/deploy/models"

app = Flask(__name__)
# Load the model
ml_model = pickle.load(open(MODEL_FILE_ROOT+'/randomForestModel.pkl','rb'))



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

from tensorflow import keras

dl_model = keras.models.load_model(MODEL_FILE_ROOT+'/simple_rnn')

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
    """Replace all interger occurrences in list of tokenized words with textual representation"""
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
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
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



def normalize_text(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_numbers(words)
    words = remove_stopwords(words)
    #words = stem_words(words)
    #words = lemmetize_verbs(words)
    return words

def text_prepare(text):
    text = denoise_text(text)
    text = ' '.join([x for x in normalize_text(tokenize(text))])
    return text


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/isalive')
def isAlive():
    data = {"status":"Live"}
    # response = app.response_class(
    #     response=json.dumps(data),
    #     status=200,
    #     mimetype='application/json'
    # )
    return jsonify(data)

@app.route('/predict',methods=['POST'])
def getPrediction():
    # Get the data from the POST request.
    data = request.get_json(force=True) 
    output = customResponse.ask_bot(data['text'])
    if output == "others":
        output = predict(data) #predict from ML model
    #output = predict_from_dl_model(data)
    #text = text_prepare(data['text'])
    #output = dl_predict.predict_with_dl_model(text)
    response = {"prediction":str(output)}
    return jsonify(response)

def humanize_output(risk_category):
    if risk_category == 0:
        return "Don't worry, there is no risk (Category I)"
    elif risk_category == 1:
        return "Don't worry, there is little risk (Category II)"
    elif risk_category == 2:
        return "There is a mild risk. (Category III)"
    elif risk_category == 3:
        return "There is risk ! (Category IV)"
    elif risk_category == 4:
        return "Be careful, it is risky !! (Category V)"


def predict(data):
    # Make prediction using model loaded from disk as per the data.
    text = text_prepare(data['text'])
    vectorizer = pickle.load(open(MODEL_FILE_ROOT+"/vector.pkl", "rb"))
    desc_vectors = vectorizer.transform([text])
    prediction = ml_model.predict(desc_vectors)
    # Take the first value of prediction
    risk_category = prediction[0]
    #risk_category =1;
    risk_category_str = humanize_output(risk_category)
    return risk_category_str

def predict_from_dl_model(data):
    # Make prediction using model loaded from disk as per the data.
    #print(data['text'])
    text = text_prepare(data['text'])
    vectorizer = pickle.load(open(MODEL_FILE_ROOT+"/vector.pkl", "rb"))
    desc_vectors = vectorizer.transform([text])
    prediction = dl_model.predict(desc_vectors)
    # Take the first value of prediction
    risk_category = prediction[0]
    risk_category_str = humanize_output(risk_category)
    return risk_category_str

if __name__ == '__main__':
    #test_predict()
    # if running on docker uncomment below line
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port,host='0.0.0.0', debug=False)

    # if running standalone uncomment below line and comment above line
    #app.run(port=5000,host='127.0.0.1', debug=True)
