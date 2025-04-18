import pickle
import os

model1_path=os.path.join(os.path.dirname(__file__),'model1.pkl')
model2_path=os.path.join(os.path.dirname(__file__),'model2.pkl')

with open(model1_path,'rb') as f:
    model1= pickle.load(f)

with open(model2_path,'rb') as g:
    model2= pickle.load(g)

def predict_model1(input_data):
    prediction = model1.predict([input_data])
    return prediction[0]

def predict_model2(input_data):
    # prediction = model2.predict([input_data])
    return "model2"