from flask import Flask,render_template,jsonify,request
import pickle
import numpy as np
from model.model import predict_model1,predict_model2
app = Flask(__name__) 
 

@app.route("/") 
def home():
    return render_template('index.html')
@app.route("/about") 
def about():
    return render_template('about.html')
@app.route("/live") 
def live():
    return render_template('live.html')

@app.route("/predictTrend",methods=['POST'])
def predicttrend():
    data = request.json
    input_data=data['features']
    result=predict_model1(input_data)
    return jsonify({'message': result})

@app.route("/predictIOT",methods=['POST'])
def predictIOT():
    data = request.json
    input_data=data['features']
    result=predict_model2(input_data)
    return jsonify({'message': result})


    


if __name__ == "__main__":
    app.run(debug=True)  
