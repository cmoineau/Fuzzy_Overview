import matplotlib.pyplot as plt
from rewriterFromCSV import RewriterFromCSV as rwCSV
from vocabulary import *
from flight import Flight

if __name__ == '__main__':
    vocab = ["DayOfWeek", "DepTime", "ArrTime", "AirTime", "ArrDelay", "DepDelay", "Distance",\
             "Month", "DayOfMonth", "TaxiIn", "TaxiOut", "CarrierDelay", "WeatherDelay", "SecurityDelay",\
             "LateAirCraftDelay"]
    path_vocabulary = "./Data/FlightsVoc2.txt"
    path_data = "./Data/2008short.csv"
    voc = Vocabulary(path_vocabulary)
    rw = rwCSV(voc, path_data)
    labels = []
    values = []
    voc_to_filter = input('Vocabulaire sur lequel filtrer les resultats :')
    while voc_to_filter not in vocab:
        print("Please use one of these key word :")
        print(vocab)
        voc_to_filter = input("Vocabulaire sur lequel filtrer les resultats :")
    for label, x in rw.R.items():
        if label.split(".")[0] == voc_to_filter:
            labels.append(label.split(".")[1])
            values.append(x)

    plt.figure(figsize=(10, 10))
    plt.pie(values, labels=labels,
            autopct='%1.1f%%', startangle=200)
    plt.title("Description of the " + voc_to_filter, fontsize=15)
    plt.show()