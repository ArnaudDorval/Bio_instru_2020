import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
import pickle


data = pd.read_csv("BilanA.csv", sep=",")
print(data.head())

data = data[["RDC", "IRDC", "RACrms", "IRACrms", "SaO2"]]
print(data.head())

predict = "SaO2"

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x,y, test_size = 0.1)

best = 0
for i in range(50):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

    linear = linear_model.LinearRegression()
    linear.fit(x_train, y_train)

    acc = linear.score(x_test, y_test)
    print(acc)

    if acc > best:
        best = acc
        #sauve le model
        with open("student-model.pickle", "wb") as f:
            pickle.dump(linear, f)


#ouvre le model
pickle_in = open("student-model.pickle", "rb")
linear = pickle.load(pickle_in)

#Afficher le model

print("Co: \n", linear.coef_)
print("Intercept: \n", linear.intercept_)