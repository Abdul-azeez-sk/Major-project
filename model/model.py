import pickle
import os

model1_path=os.path.join(os.path.dirname(__file__),'price_predictor.pkl')

with open(model1_path,'rb') as f:
    model1= pickle.load(f)


def predict_model1(input_data):
    import numpy as np
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model1.predict(input_array)
    return float(prediction[0])
