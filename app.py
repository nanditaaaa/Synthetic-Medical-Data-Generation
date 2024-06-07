from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('templates/model.pkl', 'rb'))

@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict_proba(final)
    output = '{:.2f}'.format(prediction[0][1])

    if prediction[0][1] > 0.5:
       pred_message = 'You are Diabetic.\nProbability of diabetes occurring is {:.2f}'.format(prediction[0][1])
    else:
       pred_message = 'You are not Diabetic.\nProbability of diabetes occurring is {:.2f}'.format(prediction[0][1])

    return render_template('index.html', pred=pred_message, bhai="kuch karna hain iska ab?")

if __name__ == '__main__':
    app.run(debug=True)
    
