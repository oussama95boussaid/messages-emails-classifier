from flask import Flask, request, render_template
# import numpy as np
# import pandas as pd
# import re
# import json
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from sklearn.metrics import classification_report,confusion_matrix
# import nltk
# from bs4 import BeautifulSoup
# from keras.models import load_model
# from nltk.corpus import stopwords
# nltk.download('stopwords')


app = Flask(__name__,template_folder='template')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract input email from the request
    email = str(request.form['message'])
    print(email)

    # Preprocess the input features
    # Make predictions using the loaded model
    # prediction = model.predict([[feature1, feature2]])

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
