#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import sys
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
        self.readAndRewrite()

    def readAndRewrite(self):
        for part in self.vocabulary.getPartitions():
            for partelt in part.getModalities():
                self.R[part.attname + "." + partelt.getName()] = 0
        try:
            with open(self.dataFile, 'r') as source:
                nb_row = 0
                for line in source:
                    nb_row += 1
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        f_rewrite = f.rewrite()
                        for key in f_rewrite:
                            self.R[key] += f_rewrite[key]
            for key, elts in self.R.items():
                    self.R[key] = elts / nb_row
        except:
            raise Exception("Error while loading the dataFile %s" % (self.dataFile))

    def correlation(self, v1, v2):
        """
        Cette fonction va calculer la correlation entre deux conditions v1 et v2
        :param v1:
        :param v2:
        :return:
        """
        Rv1={}
        for i in v1:
            Rv1[i] = 0
        # Calcul de cover(v1, Rv2) & cover(v1, R)
        Rv1 = rw.recriture(v1)

        cover1 = 0
        cover2 = 0
        for key, elts in Rv1.items():
            cover2 += self.R[key]
            if key in v2:
                cover1 += elts
        cover1 = cover1 / len(Rv1)
        cover2 = cover2 / len(self.R)
        # Calcul de dep(v1,v2)
        dep = cover1 / cover2
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
        s = rw.selection(list_id,seuil=seuil)
        for flight in selection :
            f = flight.rewrite()
            for key,x in f.items() :
                ans[key]= ans[key] + x/len(selection)
        return ans


if __name__ == "__main__":
    path_vocabulary = "./Data/FlightsVoc2.txt"
    path_data = "./Data/testData"
    if os.path.isfile(path_vocabulary):
        voc = Vocabulary(path_vocabulary)
        if os.path.isfile(path_data):
            rw = RewriterFromCSV(voc, path_data)
            # rw.readAndRewrite()
            selection = rw.selection(['DayOfWeek.end'])
            print(rw.reecriture(['DayOfWeek.end']))

            #for flight in selection:
            #    print(flight.fields['TailNum'])
            # print(rw.correlation(['DepDelay.long'], ['ArrDelay.long']))
        else:
            print("Data file %s not found" % path_data)
    else:
        print("Voc file %s not found" % path_data)
