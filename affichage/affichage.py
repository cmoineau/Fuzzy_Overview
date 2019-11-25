import matplotlib.pyplot as plt
from rewriterFromCSV import RewriterFromCSV as rwCSV
from vocabulary import *
import numpy as np

vocab = ["DayOfWeek", "DepTime", "ArrTime", "AirTime", "ArrDelay", "DepDelay", "Distance",\
             "Month", "DayOfMonth", "TaxiIn", "TaxiOut", "CarrierDelay", "WeatherDelay", "SecurityDelay",\
             "LateAirCraftDelay"]
path_vocabulary = "../Data/FlightsVoc2.txt"
path_data = "../Data/2008short.csv"
print('Loading vocabulary ...')
voc = Vocabulary(path_vocabulary)
part_name = []
for part in voc.getPartitions():
    for partelt in part.getModalities():
        part_name.append(part.attname + "." + partelt.getName())
print('Loading data ...')
rw = rwCSV(voc, path_data)


def show_pie ():
    '''
    Allow a visualisation of a partition
    :return:
    '''
    labels = []
    values = []
    voc_to_filter = ""
    while voc_to_filter not in vocab:
        print("Please use one of these key word :")
        print(vocab)
        voc_to_filter = input("Vocabulaire sur lequel filtrer les resultats : ")
    for label, x in rw.readAndRewrite().items():
        if label.split(".")[0] == voc_to_filter:
            labels.append(label.split(".")[1])
            values.append(x)
    plt.figure(figsize=(10, 10))
    plt.pie(values, labels=labels,
            autopct='%1.1f%%', startangle=200)
    plt.title("Description of the " + voc_to_filter, fontsize=15)
    plt.show()


def plot_pie(partition):
    '''
    Create a visualisation of the partition
    :return:
    '''
    labels = []
    values = []
    for label, x in rw.readAndRewrite().items():
        if label.split(".")[0] == partition:
            labels.append(label.split(".")[1])
            values.append(x)
    plt.figure(figsize=(10, 10))
    plt.pie(values, labels=labels,
            autopct='%1.1f%%', startangle=200)
    plt.title("Description of the " + partition, fontsize=15)
    plt.show()

def plot_heat_map(partition1, partition2):
    '''
    Create a visualisation of the correlation between two partitions
    :return:
    '''
    column_labels = []
    row_labels = []
    for p in part_name:
        if p.split('.')[0] == partition1:
            row_labels.append(p.split('.')[1])
        if p.split('.')[0] == partition2:
            column_labels.append(p.split('.')[1])
    data = []
    for mod1 in row_labels:
        t=[]
        for mod2 in column_labels:
            correl = rw.correlation([partition1 + '.' + mod1], [partition2 + '.' + mod2])
            if correl == 'error':  # TODO : trouver une façon plus élégante de gérer les erreurs
                correl = 0
            t.append(correl)
        data.append(t)
    data = np.array(data)
    fig, axis = plt.subplots()  # il me semble que c'est une bonne habitude de faire supbplots
    heatmap = axis.pcolor(data, cmap=plt.cm.Greens)  # heatmap contient les valeurs

    axis.set_yticks(np.arange(data.shape[0]) + 0.5, minor=False)
    axis.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)

    axis.invert_yaxis()

    axis.set_yticklabels(row_labels, minor=False)
    axis.set_xticklabels(column_labels, minor=False)

    axis.set_ylabel(partition1)
    axis.set_xlabel(partition2)
    axis.set_title('Corrélation entre ' + partition1 + ' et ' + partition2)
    fig.set_size_inches(11.03, 3.5)
    plt.show()

def coeff_corell (v):  # TODO : Il faut en pas calculer la corrélation ave lui même !
    dico_coeff = {}
    for p in part_name:
        if not p== v:
            dico_coeff[p] = rw.correlation([v], [p])
    return dico_coeff

