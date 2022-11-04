from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import json
from fintech_model import Fintech


app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def makecalc():
    data = request.get_json()
    prediction = np.array2string(model.predict(data))

    # data = {}

    # data['int_rate'] = form.int_rate.data
    # data['loan_amnt'] = form.loan_amnt.data
    # data['term'] = 36 if form.term.data == None else 60
    # data['fund_rate'] = form.fund_rate.data
    # data['bc_open_to_buy'] = form.bc_open_to_buy.data
    # data['total_il_high_credit_limit'] = form.total_il_high_credit_limit.data
    # data['dti'] = form.dti.data
    # data['annual_inc'] = form.annual_inc.data
    # data['bc_util'] = form.bc_util.data

    fin = Fintech()
    res = fin.run(data)
    if res:
        result = {'status': 'success', 'data': str(round(res[0], 3))}
    else:
        result = {'status': 'failed', 'data':''}

    return jsonify(result)
    # return jsonify(prediction)

if __name__ == '__main__':
    # modelfile = 'models/final_prediction.pickle'
    modelfile = 'model.pkl'
    model = p.load(open(modelfile, 'rb'))
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0')
