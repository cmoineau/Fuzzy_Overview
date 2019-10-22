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
        self.dico = {}
        for part in self.vocabulary.getPartitions():
            for partelt in part.getModalities():
                self.dico[part.attname + "." + partelt.getName()] = 0

    def readAndRewrite(self):
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
                            self.dico[key] += f_rewrite[key]
            for key, elts in self.dico.items():
                    self.dico[key] = elts / nb_row
            print(self.dico)
        except:
            raise Exception("Error while loading the dataFile %s" % (self.dataFile))

    def t_norme(self, att1, att2):
        return min(att1, att2)

    def t_conorme(self, att1, att2):
        return max(att1,att2)

    def resume(self, list_id, seuil=0):
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


if __name__ == "__main__":
    path_vocabulary = "./Data/FlightsVoc2.txt"
    path_data = "./Data/testData"
    if os.path.isfile(path_vocabulary):
        voc = Vocabulary(path_vocabulary)
        if os.path.isfile(path_data):
            rw = RewriterFromCSV(voc, path_data)
            #rw.readAndRewrite()
            selection = rw.resume(['DepTime.morning'])
            for flight in selection:
                print(flight.fields['TailNum'])
        else:
            print("Data file %s not found" % path_data)
    else:
        print("Voc file %s not found" % path_data)
