import matplotlib.pyplot as plt
from rewriterFromCSV import RewriterFromCSV as rwCSV
from vocabulary import *
import plotly.offline as py
import plotly.graph_objs as go

vocab = ["DayOfWeek", "DepTime", "ArrTime", "AirTime", "ArrDelay", "DepDelay", "Distance",\
             "Month", "DayOfMonth", "TaxiIn", "TaxiOut", "CarrierDelay", "WeatherDelay", "SecurityDelay",\
             "LateAirCraftDelay"]
path_vocabulary = "../Data/FlightsVoc2.txt"
path_data = "../Data/2008short.csv"
print('Loading vocabulary ...')
voc = Vocabulary(path_vocabulary)
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


def plot_pie (partition):
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


def show_sunburst():
    '''
    Not really functionnal need the full database
    :return:
    '''
    labels = []
    values = []
    parents = []
    voc_to_filter = "DepDelay.short"
    # while voc_to_filter not in vocab:
    #     print("Please use one of these key word :")
    #     print(vocab)
    #     voc_to_filter = input("Keyword you want to see :")
    labels.append(voc_to_filter)
    parents.append("")
    values.append(0)

    month = ["Month.autumn", "Month.winter", "Month.spring", "Month.summer"]
    dmonth = ["DayOfMonth.beginning", "DayOfMonth.middle", "DayOfMonth.end"]
    dweek = ["DayOfWeek.beginning", "DayOfWeek.end", "DayOfWeek.weekend"]
    for m in month:
        print(m + '\n====================')
        labels.append(m)
        parents.append(voc_to_filter)
        values.append(rw.reecriture([m])[m])
        for dm in dmonth:
            print(dm + '\n====================')
            labels.append(dm)
            parents.append(m)
            values.append(rw.reecriture([m, dm])[m])
            for d in dweek:
                print(d)
                labels.append(d)
                parents.append(dm)
                values.append(rw.reecriture([m, dm, d])[d])
    print(values)
    trace = go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        outsidetextfont={"size": 20, "color": "#377eb8"},
        marker={"line": {"width": 2}},
    )
    layout = go.Layout(
        margin=go.layout.Margin(t=0, l=0, r=0, b=0)
    )
    print('test 1')
    py.plot(go.Figure([trace], layout))
    print('test 1')


if __name__ == '__main__':
    print("begin")
    # show_sunburst()
    show_pie()
    print("end")