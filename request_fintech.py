import requests
import json

url = 'http://0.0.0.0:5000/api/'


int_rate = 'int_rate'
loan_amnt = 'loan_amnt'
term = 'term'
fund_rate = 'fund_rate'
bc_open_to_buy = 'bc_open_to_buy'
total_il_high_credit_limit = 'total_il_high_credit_limit'
dti = 'dti'
annual_inc = 'annual_inc'
bc_util = 'bc_util'
keys = [int_rate, loan_amnt, term, fund_rate, bc_open_to_buy,
	total_il_high_credit_limit, dti, annual_inc, bc_util]
data = [14.34, 15000, 36, 25.0, 98.0, 2.8, 1.31, 0.53, 10]

send_data = dict(zip(keys, data))

j_data = json.dumps(send_data)
print(j_data)
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
r = requests.post(url, data=j_data, headers=headers)
print(r, r.text)