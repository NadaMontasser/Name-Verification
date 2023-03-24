
import numpy as np
from flask import Flask, request, jsonify
from joblib import load
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf
from flask import  render_template
import itertools
import sys, os

current_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(current_directory))

app = Flask(__name__)
model = tf.keras.models.load_model('verification_model.h5')
bow_vectorizer = load('Bow_vectorizer.joblib')
tfidf_vectorizer = load('tfidf_vectorizer.joblib')


def add_padding(X):
  return np.array(list(zip(*itertools.zip_longest(*X , fillvalue=0))))

@app.route('/')
def homepage():
    return render_template('temp.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    name = request.form['Full Name']

    new_name = bow_vectorizer.transform([name]).toarray()
    new_name = tfidf_vectorizer.transform(new_name).toarray()

    # Make a prediction with the model
    prediction = model.predict(new_name)[0][0]

    if prediction >= 0.6:
        output= f"{name}  is a real name with high confidence"
        return render_template('temp.html', Output = output)
   #second case is that the one or two names in the full name are correct
    elif prediction > 0.3 and prediction < 0.6:
        output= f"{name}  is a real name with meduim confidence,at least one name is correct"
        return render_template('temp.html', Output = output)
   #third case is that all three names in the full name are Incorrect
    else: 
     output= f"{name}  is a real name with low confidence"
     return render_template('temp.html', Output = output)



@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict(bow_vectorizer.transform([data['text_input']]))
    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)