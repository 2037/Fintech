# README

## Credit risk predictor
This project aims to predict the risk of loan given personal credit history, which is refered as a secondary credit model populated among the P2P loan investors. I used XGBoost, an efficient Gradient Boosting Decision Tree, as the predictor based on 206k credit records. The Web App is written in flask. It would be hosted on AWS ElasticBeanstalk. 

The application is deployed on http://jackwang2037.com/projects/.

## Model deployement API

* Run `run_fintech.py` to start the server

* Model result API
	* Endpoint: http://127.0.0.1:5000/predict/
	* GET method
	* return 'safe' or 'high risk' comparing possibility and threshold
	* example request: {"int_rate": 0.34, "loan_amnt": 15000, "term": 36, "fund_rate": 0.4, "bc_open_to_buy": 9.0, "total_il_high_credit_limit": 2.8, "dti": 1.31, "annual_inc": 66, "bc_util": 10000}


* Threshold update API
	* Endpoint: http://127.0.0.1:5000/threshold
	* GET method
		* Retrieve current threshold
	* POST method
		* Update threshold
		* Payload body format: {"threshold": 0.1}

* Model update API
	* Endpoint: http://127.0.0.1:5000/model-upload
	* POST method
		* Update model
		* Payload body format: form-data, file, value is the pickle file


* Feature update API
	* Endpoint: http://127.0.0.1:5000/feature-upload
	* POST method
		* Update feature
		* Payload body format: form-data, file, value is the pickle file
