from flask import Flask,render_template,jsonify,request, send_file
import pickle
import numpy as np
from model.model2.IotSIm import generate_hourly_data
app = Flask(__name__) 
 

@app.route("/") 
def home():
    return render_template('index.html')

@app.route("/iot")
def iot():
    return render_template('iot.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/live")
def live():
    return render_template('live.html')


@app.route("/generate", methods=["POST"])
def generate():
    data = request.form  # or request.json if you're using JSON
    seeding_date = data.get("seeding_date")
    harvesting_date = data.get("harvesting_date")
    crop_id = data.get("crop_id")

    if not (seeding_date and harvesting_date and crop_id):
        return jsonify({"error": "Missing parameters"}), 400

    df = generate_hourly_data(seeding_date, harvesting_date, crop_id)
    file_path = "static/tomato_data.csv"
    df.to_csv(file_path, index=False)
    return send_file(file_path, as_attachment=True)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.form
    return 
    


if __name__ == "__main__":
    app.run(debug=True)  
