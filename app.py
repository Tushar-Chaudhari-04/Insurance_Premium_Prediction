from flask import Flask,render_template,request,jsonify,json
import pandas as pd
import numpy as np
import pickle

from sklearn.preprocessing import OrdinalEncoder

import warnings
warnings.filterwarnings('ignore')

app=Flask(__name__)

model=pickle.load(open("medical_insurance.pkl",'rb'))

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
   try:
      # Check if the request contains JSON data
      if request.is_json:
            data = request.get_json()
      else:
            # If not JSON, get data from form
            data = request.form

      age=int(request.form['age']),
      sex=1 if request.form['sex']=='male' else 0,
      bmi=float(request.form['bmi']),
      children=int(request.form['children']),
      smoker=1 if request.form['smoker']=='yes' else 0,
      region_mapping = {'northeast': 0.0, 'northwest': 1.0,'southeast': 2.0,'southwest': 3.0}
      region = region_mapping[request.form['region']]

      features=[age[0],sex[0],bmi[0],children[0],smoker[0],region]

      input_data = np.array(features).reshape(1,-1)

      # Make a prediction
      prediction = model.predict(input_data)
      predicted_original_value=np.expm1(prediction)

      # return jsonify({"predicted_cost": round(predicted_original_value[0], 2)})
      return render_template('index.html', prediction_text=f'Predicted Insurance Premium: ${predicted_original_value[0]:.2f}')
   except Exception as e:
      print("Exception ",e)
      return render_template('index.html', error_text=f'Error: {str(e)}')

if __name__=="__main__":
   app.run(debug=True)