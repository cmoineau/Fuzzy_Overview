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

    def readAndRewrite(self):
        try:
            with open(self.dataFile, 'r') as source:
                tmp_tab = []
                nb_row = 0
                for line in source:
                    nb_row += 1
                    line = line.strip()
                    if line != "" and line[0] != "#":
                        f = Flight(line, self.vocabulary)
                        # TODO : Do what you need with the rewriting vector here ...
                        f_rewrite = f.rewrite()
                        if tmp_tab:
                            for i in range(len(f_rewrite)):
                                tmp_tab[i] += f_rewrite[i]
                        else:
                            tmp_tab = f_rewrite
            cpt = 0
            for part in self.vocabulary.getPartitions():
                for partelt in part.getModalities():
                    self.dico[part.attname + "." + partelt.getName()] = (tmp_tab[cpt] / nb_row)
                    cpt += 1
            print(self.dico)
        except:
            raise Exception("Error while loading the dataFile %s" % (self.dataFile))


if __name__ == "__main__":
    path_vocabulary = "./Data/FlightsVoc2.txt"
    path_data = "./Data/2008short.csv"
    if os.path.isfile(path_vocabulary):
        voc = Vocabulary(path_vocabulary)
        if os.path.isfile(path_data):
            rw = RewriterFromCSV(voc, path_data)
            rw.readAndRewrite()
        else:
            print("Data file %s not found" % path_data)
    else:
        print("Voc file %s not found" % path_data)
