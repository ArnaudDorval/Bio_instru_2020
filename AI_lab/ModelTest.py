import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
import pickle
from matplotlib import style

data = pd.read_csv("BilanB.csv", sep=",")
#print(data.head())

data = data[["RDC", "IRDC", "RACrms", "IRACrms", "SaO2"]]
#print(data.head())

predict = "SaO2"

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y, test_size = 0.1)

#ouvre le model
pickle_in = open("student-model.pickle", "rb")
linear = pickle.load(pickle_in)

#Afficher le model

prediction = linear.predict(x)


for i in range(len(prediction)):
    print(prediction[i], y[i])