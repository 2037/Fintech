from flask import redirect,url_for
from flask import Flask, request, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename
import os
import numpy as np
import pandas as pd
import pickle as p
import xgboost as xgb
from flask import render_template

app = Flask(__name__,template_folder='templates')

MODEL_FOLDER = './models'
FEATURE_FOLDER = './features'
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['FEATURE_FOLDER'] = FEATURE_FOLDER

feature_file_path = './features/feature.pkl'
model_file_path = './models/model.pkl'


# global threshold
threshold = 0.1
# default prediction data
prediction_param = None
prediction_result = {'high_risk': 0.09, 'safe': 0.91, 'threshold': 0.1}

# login data
adminName = 'admin'
adminPassWord = 'admin'
userName = 'demo'
userPassWord = '123456'

@app.route('/predict', methods=['POST'])
@cross_origin()
def makecalc():
    global prediction_param,prediction_result
    
    # data = request.get_json() # used in return as 
    data_from_request = request.form.to_dict()
    data = {}
    for a,x in data_from_request.items():
        data.update({a:float(x)})
    # print(data)
    prediction_param = data 

    feature_path = feature_file_path
    feature = pd.read_pickle(feature_path)

    # fix feature
    feature['bc_open_to_buy'] = data['bc_open_to_buy']
    feature['total_il_high_credit_limit'] = data['total_il_high_credit_limit']
    feature['dti'] = data['dti']
    feature['annual_inc'] = data['annual_inc']
    feature['bc_util'] = data['bc_util']

    feature['int_rate'] = data['int_rate']/100
    # high wie
    if data['term'] == 36:
        feature['term_ 36 months'] = 1
        feature['term_ 60 months'] = 0
    else:
        feature['term_ 36 months'] = 0
        feature['term_ 60 months'] = 1

    feature['loan_amnt'] = data['loan_amnt']
    
    loan_rate = data['fund_rate']/100
    feature['funded_amnt'] = loan_rate * feature['loan_amnt']

    dtrain = xgb.DMatrix(feature, missing=np.NAN)

    modelfile = model_file_path
    model = p.load(open(modelfile, 'rb'))

    prediction = model.predict(dtrain)
    prediction = float(prediction)

    #jsonify if need return json 
    prediction_result = {'high_risk': round(prediction, 2),
                        'safe': round(1 - prediction, 2),
                        'threshold': threshold}

    return redirect(url_for('index'))
    # return redirect(url_for('homepage'))


@app.route('/threshold', methods=['POST', 'GET'])
@cross_origin()
def update_thres():
    global threshold
    new_thres = 0
    try:
        new_thres = float(request.form['threshold'])
    except:
        pass
    
    if request.method == 'POST':
        threshold = new_thres
        # print(url_for('homepage'))
        # url_for('homepage')
        # return redirect(url_for('.index')) #url for function name
        # return redirect("https://www.google.com") #url for function name
        return redirect(url_for('index')) #url for function name

        # return jsonify(threshold)
    elif request.method == 'GET':
        return jsonify(threshold)



@app.route('/model-upload', methods=['POST'])
@cross_origin()
def upload_model():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file :
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['MODEL_FOLDER'], filename))
        resp = jsonify({'message' : 'Model successfully uploaded'})
        resp.status_code = 201
        return resp
    

@app.route('/feature-upload', methods=['POST'])
@cross_origin()
def upload_feature():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file :
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['FEATURE_FOLDER'], filename))
        resp = jsonify({'message' : 'Feature set successfully uploaded'})
        resp.status_code = 201
        return resp


@app.route('/',methods=["GET","POST"])
@app.route('/index',methods=["GET","POST"])
@cross_origin()
def index():
    global threshold,prediction_result

    # update prediction and threshold
    prediction_str = f"{prediction_result['high_risk']*100}%"
    threshold_str = f"{threshold*100}%"
    loan_status = "Unknown"

    # update status
    if(prediction_result['high_risk'] <= threshold):
        loan_status = 'Safe'
    else:
        loan_status = 'Dangerous'

    # test return from param
    return render_template("index.html",
        current_threshold = threshold_str,
        prediction_json = prediction_str,
        prediction_param = prediction_param,
        loan_status = loan_status,
    )

if __name__ == '__main__':
    threshold = 0.1
    app.run()
    # app.run(debug=True, host='0.0.0.0')