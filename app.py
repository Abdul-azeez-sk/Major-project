from flask import Flask,render_template,jsonify,request, send_file
import numpy as np
from model.model2.IotSIm import generate_hourly_data
app = Flask(__name__) 
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import seaborn as sns
from datetime import datetime, timedelta
import hashlib

class SmoothMockPriceModel:
    def predict(self, X):
        if not isinstance(X, pd.DataFrame):
            X = pd.DataFrame(X)

        def row_to_val(row):
            base_key = f"{row['AmcCode']}_{row['YardCode']}_{row['VarityCode']}"
            base_hash = int(hashlib.md5(base_key.encode()).hexdigest()[:8], 16)
            base_price = 1000 + (base_hash % 800)

            date = pd.Timestamp(year=row['Year'], month=row['Month'], day=row['Day'])
            day_of_year = date.dayofyear
            variation = 100 * np.sin(2 * np.pi * day_of_year / 30)

            price = base_price + variation
            return round(price, 2)

        preds = X.apply(row_to_val, axis=1)
        return preds.values

# Create model instance
model = SmoothMockPriceModel()

def plot_iot_data(df: pd.DataFrame, save_path):
    # Combine Date and Hour into a datetime object instead of string concatenation
    df['Timestamp'] = pd.to_datetime(df['Date'] + ' ' + df['Hour'].astype(str) + ':00')

    # Scale down CO2 by dividing by 100
    df['CO2_scaled'] = df['CO₂_ppm'] / 100

    plt.figure(figsize=(12, 6))
    plt.plot(df['Timestamp'], df['Temperature_°C'], label='Temperature (°C)', color='red')
    plt.plot(df['Timestamp'], df['Humidity_%'], label='Humidity (%)', color='blue')
    plt.plot(df['Timestamp'], df['CO2_scaled'], label='CO₂ (ppm / 100)', color='green')

    plt.xlabel('Timestamp')
    plt.ylabel('Sensor Values')
    plt.title('IoT Sensor Data Over Time')

    # Format x-axis dates nicely
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())   # Automatic date tick locators
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))  # Format datetime labels
    
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    if save_path:
        plt.savefig(save_path)
    plt.close()

def iot_data(df: pd.DataFrame):
        # Assuming df is your loaded DataFrame and Timestamp is datetime dtype
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    # 1. Time Series line plots
    fig, axs = plt.subplots(5, 1, figsize=(15, 20), sharex=True)
    variables = ['Temperature_°C', 'Humidity_%', 'CO2_scaled', 'Soil_Moisture_%', 'Light_lux']
    for ax, var in zip(axs, variables):
        ax.plot(df['Timestamp'], df[var], label=var)
        ax.set_ylabel(var)
        ax.legend()
    plt.xlabel('Timestamp')
    plt.suptitle('Time Series of Environmental Variables')
    plt.savefig('static/1')
    # 2. Correlation heatmap
    plt.figure(figsize=(8,6))
    corr = df[['Temperature_°C', 'Humidity_%', 'CO2_scaled', 'Soil_Moisture_%', 'Light_lux']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig('static/2')

    # 3. Boxplots by Period
    plt.figure(figsize=(12,8))
    for i, var in enumerate(variables, 1):
        plt.subplot(2,3,i)
        sns.boxplot(x='Period', y=var, data=df)
        plt.title(f'{var} distribution by Period')
    plt.tight_layout()
    plt.savefig('static/3')
    # 4. Scatter plot CO2_scaled vs Temperature, colored by Period
    plt.figure(figsize=(8,6))
    sns.scatterplot(x='Temperature_°C', y='CO2_scaled', hue='Period', data=df)
    plt.title('CO2_scaled vs Temperature')
    plt.savefig('static/4')
    # 5. Hourly averages
    hourly_avg = df.groupby('Hour')[variables].mean().reset_index()
    plt.figure(figsize=(12,8))
    for var in variables:
        plt.plot(hourly_avg['Hour'], hourly_avg[var], label=var)
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Value')
    plt.title('Hourly Average of Variables')
    plt.legend()
    plt.savefig('static/5')

    
@app.route("/") 
def home():
    return render_template('index.html', amcnames = amc_name_to_code , yardnames = yard_name_to_code , varieties = varity_name_to_code , crops = comm_name_to_code)

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
    
    table_html = df.to_html(classes='iot-table', index=False)
    print(df.columns.tolist())
     
    plot_iot_data(df , save_path='static/iot_sensor_plot.png')
    iot_data(df)
    file_path = "static/tomato_data.csv"
    df.to_csv(file_path, index=False)
    
    return render_template("iot.html", table=table_html, seeding_date=seeding_date,harvesting_date=harvesting_date,crop_id=crop_id,plot_image="iot_sensor_plot.png")



amc_name_to_code = {
 'Chevella': 322,
 'Ibrahimpatnam(RR)': 313,
 'Shadnagar': 310,
 'Hyderabad': 325,
 'Sangareddy': 295,
 'Kalwakurthy': 303,
 'Gudimalkapur': 367,
 'Vantimamidi': 331,
 'Bowenpally': 324,
 'Shankerpally': 319,
 'Warangal': 246,
 'Gaddiannaram': 323,
 'Venkateshwar Nagar': 281,
 'Khammam': 256,
 'Jainath': 192,
 'Patancheru': 361,
 'Gajwel': 283,
 'Madnoor': 207
}

yard_name_to_code = {
 'Chevella': 46,
 'Ibrahimpatnam': 42,
 'Shadnagar': 1330,
 'Meeralamandi': 7,
 'Madannapeta': 6,
 'Sangaredy': 1219,
 'Kalwakurthy': 1340,
 'Gudumalkapur': 1571,
 'Vantimamidi': 1612,
 'Bowenpally': 3,
 'Shankerpally': 40,
 'Warangal': 886,
 'L.B Nagar': 2,
 'V Nagar': 1106,
 'Khammam': 1067,
 'Jainath': 26,
 'Patancheru': 1613,
 'Gajwel': 1201,
 'Madnoor': 1083
}
varity_name_to_code = {'Local': 197, 'Common': 114, '618': 210, 'Hybrid': 198}
comm_name_to_code = {'Tomato': 114, 'Potato': 115}


@app.route("/predict", methods=["POST"])
def predict():
    data = request.form
    
    # Extract input parameters
    start_date_str = data.get("start_date")
    stop_date_str = data.get("stop_date")
    CommName = data.get("CommName")
    VarityName = data.get("VarityName")
    AmcName = data.get("AmcName")
    YardName = data.get("YardName")
    Arrivals = float(data.get("Arrivals", 0))

    # Convert dates to datetime objects
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    stop_date = datetime.strptime(stop_date_str, "%Y-%m-%d")

    # Load the model
    with open("model/model1/smooth_mock_price_model.pkl", "rb") as f:
        model = pickle.load(f)
    
    # Prepare dataframe for each date in range
    df_list = []
    current_date = start_date
    while current_date <= stop_date:
        df_list.append({
            'AmcCode': amc_name_to_code.get(AmcName, 0),
            'YardCode': yard_name_to_code.get(YardName, 0),
            'VarityCode': varity_name_to_code.get(VarityName, 0),
            'Year': current_date.year,
            'Month': current_date.month,
            'Day': current_date.day,
        })
        current_date += timedelta(days=1)
    
    df_test = pd.DataFrame(df_list)

    # Predict
    preds = model.predict(df_test)

    results = []
    for i, row in df_test.iterrows():
       results.append({
                'Date': f"{row['Year']}-{row['Month']:02d}-{row['Day']:02d}",
                'Predicted_Price': round(preds[i], 2)  
        })

    return render_template(
    "index.html",
    predictions=results,
    start_date=start_date_str,
    stop_date=stop_date_str,
    CommName=CommName,
    VarityName=VarityName,
    AmcName=AmcName,
    YardName=YardName,
    Arrivals=Arrivals
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)  
