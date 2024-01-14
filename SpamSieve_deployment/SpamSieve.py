from flask import Flask, request, render_template
import os
import numpy as np
import pandas as pd
import re
import json
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report,confusion_matrix
import nltk
from bs4 import BeautifulSoup
from keras.models import load_model
from nltk.corpus import stopwords
nltk.download('stopwords')


app = Flask(__name__,template_folder='template')

# Process the email
# remove the head of eamil
def remove_header(email):
    """remove the header from an email"""
    # return email[email.index('\n\n'):]
    return email


def remove_html_tags(input):
    soup = BeautifulSoup(input, 'html.parser')
    return soup.get_text()

# replace URLs with oussama word and emails with boussaid
def remove_hyperlink(word):
    regex_links = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    word_without_links =  re.sub(regex_links,"oussama", word)
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.sub(regex_email,"boussaid", word_without_links)


# make word in lower case
def to_lower(word):
    return word.lower()


# remove whitespaces
def remove_whitespace(word):
    return word.strip()


def remove_digits(word):
  '''This function removes all the numbers'''
  return re.sub('\d+', '', word)

def remove_underscores(word):
  '''This function removes all the underscores'''
  return re.sub(r'_', '', word)


def remove_special_characters(word):
  '''This function removes all the special characters'''
  return re.sub('\W', ' ', word)

# remove stop words
stopwords_english = stopwords.words('english')
def remove_stopwords(word,stopword_list=stopwords_english):
  '''This function removes the stop words'''
  word_list = word.split(" ")
  cleaned_txt = [w for w in word_list if not w in stopword_list]
  cleaned_string = " ".join(cleaned_txt)

  return cleaned_string

def EmailsPreprocessor(sentence):

    Preprocessor_utils = [remove_header,
                      remove_html_tags,
                      to_lower,
                      remove_hyperlink,
                      remove_whitespace,
                      remove_digits,
                      remove_underscores,
                      remove_stopwords,
                      remove_special_characters]

    for tool in Preprocessor_utils:
        sentence = tool(sentence)

    return sentence

# static/MetaData/test_data.json
word_index = os.path.join(app.static_folder, 'MetaData', 'word_index.json')

def Tokenizer_email(email):
  max_len = 3000 # max number of words in a question to use
  # Load word_index from the saved JSON file
  with open(word_index, 'r') as json_file:
      loaded_word_index = json.load(json_file)

  tokenizer = Tokenizer()
  tokenizer.word_index = loaded_word_index
  eamil_seq = np.array(tokenizer.texts_to_sequences([email]))
  # print(eamil_seq)

  return pad_sequences(eamil_seq,maxlen=max_len)


# static/MetaData/test_data.json
metadata = os.path.join(app.static_folder, 'MetaData', 'Email_classifier.h5')

def Emails_Classifier(email):
  email_pro = EmailsPreprocessor(email)
  print(email_pro)
  email_tok = Tokenizer_email(email_pro)
  print(email_tok)
  # load model's metadata
  model = load_model(metadata)
  # Model predict  a number from 0.0 to 1.0
  y_pred = model.predict(email_tok)

  print(y_pred)

  if y_pred[0] > 0.5 :
    return 'Spam'

  else :
    return 'Ham'



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input email from the request
    email = str(request.form['message'])
    print(email)
    # Make predictions using the loaded model
    pred = Emails_Classifier(email)
    
    return render_template('index.html',prediction=pred)


if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    app.run(debug=True)

