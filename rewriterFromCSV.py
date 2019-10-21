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


	def readAndRewrite(self):
		try:
			with open(self.dataFile, 'r') as source:
				for line in source:
					line = line.strip()
					if line != "" and line[0] != "#":
		
						f = Flight(line,self.vocabulary)
						##Do what you need with the rewriting vector here ...
						print(f.rewrite())

		except:
			raise Exception("Error while loading the dataFile %s"%(self.dataFile))



if __name__ == "__main__":
 	if len(sys.argv)  < 3:
 		print("Usage: python flight.py <vocfile> <dataFile>")
 	else:
 		if os.path.isfile(sys.argv[1]): 
 			voc = Vocabulary(sys.argv[1])
	 		if os.path.isfile(sys.argv[2]): 
	 			rw = RewriterFromCSV(voc, sys.argv[2])
	 			rw.readAndRewrite()
	 		else:
	 			print("Data file %s not found"%(sys.argv[2]))
	 	else:
	 		print("Voc file %s not found"%(sys.argv[2]))
