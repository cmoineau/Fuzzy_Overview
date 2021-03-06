#!/usr/bin/python
# -*- coding: utf-8 -*-
from vocabulary import *
from flight import Flight


class RewriterFromCSV(object):

    def __init__(self, voc, df):
        """
        Translate a dataFile using a given vocabulary
        """
        self.vocabulary = voc
        self.dataFile = df
        self.R = {}
        self.nb_flight = 0

    def readAndRewrite(self):
        if self.R != {}: # Here we test if we have already computed R.
            return self.R
        R = {}
        for part in self.vocabulary.getPartitions():
            for partelt in part.getModalities():
                R[part.attname + "." + partelt.getName()] = 0
        try:
            with open(self.dataFile, 'r') as source:
                self.nb_flight = 0
                for line in source:
                    self.nb_flight += 1
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        f_rewrite = f.rewrite()
                        for key in f_rewrite:
                            R[key] += f_rewrite[key]
            for key, elts in R.items():
                    R[key] = elts / self.nb_flight
        except:
            raise Exception("Error while loading the dataFile %s" % (self.dataFile))
        return R

    def correlation(self, v1, v2):
        """
        Cette fonction va calculer la correlation entre deux conditions v1 et v2
        :param v1:
        :param v2:
        :return:
        """
        Rv1 = self.reecriture(v1)
        R = self.readAndRewrite()
        size_r1 = len(self.selection(v1))
        cover1 = 0
        cover2 = 0
        for key in v2:
            cover2 += R[key]
            cover1 += Rv1[key]
        # Calcul de dep(v1,v2)
        if cover2 != 0:
            dep = cover1 / cover2
        else:
            return "error"
        # print(dep, cover1, cover2)
        if dep <= 1:
            return 0
        else:
            return 1 - (1/dep)

    def t_norme(self, att1, att2):
        return min(att1, att2)

    def t_conorme(self, att1, att2):
        return max(att1,att2)

    def selection(self, list_id, seuil=0.0):
        ans = []
        with open(self.dataFile, 'r') as source:
            for line in source:
                line = line.strip()
                if line != "" and line[0] != "#":
                    f = Flight(line, self.vocabulary)
                    f_rewrite = f.rewrite()
                    min = 1
                    for key in f_rewrite:
                        if key in list_id:
                            min = self.t_norme(min, f_rewrite[key])
                    if min > seuil:
                        ans.append(f)
        return ans

    def reecriture(self, list_id, seuil=0.0):
        ans = {}
        for part in self.vocabulary.getPartitions():
            for partelt in part.getModalities():
                ans[part.attname + "." + partelt.getName()] = 0
        s = self.selection(list_id, seuil=seuil)
        for flight in s:
            f = flight.rewrite()
            for key, x in f.items():
                ans[key]= ans[key] + x/len(s)
        return ans

    def distance(self, v1, v2):
        """
        calcul la distance séparant deux termes au sein d'une même partition. Renvoie 0
        si les termes sont identiques. Renvoie -1 s'ils n'appartiennent pas à la même partition
        :param v1: terme v1
        :param v2: terme v2
        :return: d la distance (entier) en valeur absolue entre v1 et v2
        """
        if v1.split(".")[0] == v2.split(".")[0]:
            modnames = self.vocabulary.getPartition(v1.split(".")[0]).modnames
            i1 = modnames.index(v1.split(".")[1])
            i2 = modnames.index(v2.split(".")[1])
            d = abs(i2 - i1)/(len(modnames) - 1)
        else :
            d= -1
        return d

    def atypique(self, v1):
        maxi = 0
        partition = v1.split(".")[0]
        Rv1 = self.reecriture(v1)
        c1 = Rv1[v1]

        for mod in self.vocabulary.getPartition(partition).modnames:
            if mod != v1.split(".")[1]:
                v2 = partition + "." + mod
                d = self.distance(v1, v2)
                Rv2 = self.reecriture(v2)
                c2 = Rv2[v2]
                maxi = max(min(d, c1, 1-c2), maxi)
                print(d, c1,  Rv1[v1], len(self.vocabulary.getPartitions()), 1-c2, maxi)

        return maxi


if __name__ == "__main__":
    path_vocabulary = "./Data/FlightsVoc2.txt"
    path_data = "./Data/2008short.csv"
    if os.path.isfile(path_vocabulary):
        voc = Vocabulary(path_vocabulary)
        if os.path.isfile(path_data):
            rw = RewriterFromCSV(voc, path_data)
            # rw.readAndRewrite()
            # selection = rw.selection(['DayOfWeek.end'])
            # for flight in selection:
            #     print(flight.fields['TailNum'])
            # print(rw.reecriture(['DayOfWeek.end']))
            # print(rw.correlation(['DepDelay.veryLong'], ['ArrDelay.veryLong']))
            print(rw.atypique('Origin.big'))

        else:
            print("Data file %s not found" % path_data)
    else:
        print("Voc file %s not found" % path_data)
