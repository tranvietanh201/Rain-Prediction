import os
import pickle
import pandas as pd
from sklearn.feature_selection import SelectKBest, chi2
from flask import Flask, jsonify, request
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = "xgb_model.pkl"
with open(MODEL_PATH, "rb") as rf:
    xgb = pickle.load(rf)

# Init the app
app = Flask(__name__)

# App health check
@app.route("/statuscheck", methods=["GET"])
def healthcheck():
    msg = (
        "server is running"
    )
    return jsonify({"message": msg})

# predict function
def predict_function(sample, xgb):
    
    # IMPORTANT: USE THE SUITABLE ORIENT
    test = pd.DataFrame.from_dict(sample, orient='index')
    
    
    #test1 = list(test.filter(['Rainfall','WindSpeed9am','WindSpeed3pm','Humidity3pm','RainToday']))
#     for col in test1:
#         test[col] = test[col].astype('int32')
   
    test = test.filter(['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
       'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
       'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
       'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
       'Temp3pm', 'RainToday'])
    
    # We will now lable encode the rest object columns to build model
    encoder = LabelEncoder()

    label_encoder_columns = test.columns

    for column in label_encoder_columns:
        test[column] = encoder.fit_transform(test[column])
    
    #convert columns to numpy array 
    test.Dataframe.to_numpy()
                
    # predict
    params_xgb ={'n_estimators': 500,
            'max_depth': 16}
    y_pred = xgb.predict(test)
      
    return y_pred


# Predict function api
@app.route("/predict", methods=["POST"])
def predict():
    sample = request.get_json(silent = True)
    predictions = predict_function(sample, xgb)

    result = {
        'prediction': list(predictions)
    }
    
    return jsonify(result)

#not functioning
# # evaluate function
# def evaluate_function(sample, clf):
    
#     # IMPORTANT: USE THE SUITABLE ORIENT
#     test = pd.DataFrame.from_dict(sample, orient='index')

#     # if you have any step of data transformation, include it here
#     test = test.filter(['Location', 'MinTemp', 'MaxTemp', 'Rainfall', 'Evaporation', 'Sunshine',
#        'WindGustDir', 'WindGustSpeed', 'WindDir9am', 'WindDir3pm',
#        'WindSpeed9am', 'WindSpeed3pm', 'Humidity9am', 'Humidity3pm',
#        'Pressure9am', 'Pressure3pm', 'Cloud9am', 'Cloud3pm', 'Temp9am',
#        'Temp3pm', 'RainToday'])   
 
#     # separate features / label column here:
#     X_test = test.drop['RainTomorrow']
#     y_test = test['RainTomorrow']
    
     
#     # We will now lable encode the rest object columns to build model
#     encoder = LabelEncoder()

#     label_encoder_columns = test.columns

#     for column in label_encoder_columns:
#         test[column] = encoder.fit_transform(test[column])
    
#     #convert column to numpy
#     test.Dataframe.to_numpy()
                
#     # predict
#     y_pred = xgb.predict(X_test)
    
#     # evaluate
#     from sklearn.metrics import accuracy_score
#     accuracy = accuracy_score(y_test, y_pred)
    
#     return accuracy



# # evaluate function api
# @app.route("/evaluate", methods=["POST"])
# def evaluate():
#     sample = request.get_json
#     accuracy = evaluate_function(sample, clf)

#     result = {
#         'accuracy': accuracy
#     }
    
#     return jsonify(result)

# main
if __name__ == '__main__':
    app.run(debug=True)