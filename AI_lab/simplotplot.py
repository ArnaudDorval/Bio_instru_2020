


#checker les donnees
data = pd.read_csv(selection + ".csv", sep=",")
data = data[["TAG", "Value", "Time"]]

y_data = "Value"
x_data = "Time"

style.use("ggplot")
pyplot.scatter(data[x_data], data[y_data])
pyplot.xlabel(x_data)
pyplot.ylabel(y_data)
pyplot.show()