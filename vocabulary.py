#!/usr/bin/python

import sys
import os


class Modality(object):

    def __init__(self, modname):
        self.modname = modname
        self.estimatedCardinality = None

    def getEstimatedCardinality(self):
        return self.estimatedCardinality

    def setEstimatedCardinality(self, c):
        self.estimatedCardinality = c

    def getName(self):
        return self.modname

    def getMu(self, *args):
        raise Exception("This class is abstract")

    def getIntersection(self, *args):
        raise Exception("This class is abstract")

    def getDerivedPredicate(self, alpha=0):
        raise Exception("This class is abstract")

    def __repr__(self):
        return self.__str__()


class TrapeziumModality(Modality):
    "This class represents a modality of an attribute, ex: 'young' for attribute 'age' represented by a trapezium"

    def isTrapeziumModality(self):
        return True
    def isEnumModality(self):
        return False
    
    def __init__(self, modname, minSupport, minCore, maxCore, maxSupport):
        Modality.__init__(self, modname)
        self.minSupport = minSupport
        self.minCore = minCore
        self.maxCore = maxCore
        self.maxSupport = maxSupport

    def getDerivedPredicate(self, alpha=0):
        eps=0.0001
        mi = self.minSupport + ((self.minCore - self.minSupport) * alpha)
        ma = self.maxSupport - ((self.maxSupport - self.maxCore) * alpha)
        if alpha == 0:
            mi = mi+eps
            ma = ma-eps
        return " BETWEEN "+str(mi)+" AND "+ str(ma)

    def getMu(self, v):
        "returns the satisfaction degree of v to this modality"
        ret=0.0
        if v is None: 
            ret=0.0
        else:
            v = float(v)
            # est-ce que la modalité est inversée ?
            if self.maxSupport < self.minSupport:
                if v >= self.minCore or v <= self.maxCore:
                    # in the core
                    ret=1.0            
                elif v >= self.minSupport:
                    # left to the core
                    ret = 1.0 - ((self.minCore - v) / (self.minCore - self.minSupport))
                elif v <= self.maxSupport:
                    # right to the core
                    ret =  (self.maxSupport - v) / (self.maxSupport - self.maxCore)
                # out of the support
                else:
                    ret= 0.0
            else:
                # modalité normale
                if v > self.maxSupport or v < self.minSupport:
                    # out of the support
                    ret = 0.0
                elif v < self.minCore:
                    # left to the core
                    ret = (v - self.minSupport) / (self.minCore - self.minSupport)
                elif v > self.maxCore:
                    # right to the core
                    ret = (self.maxSupport - v) / (self.maxSupport - self.maxCore)
                # in the core
                else:
                    ret=1.0
        return ret


    def getIntersection(self, lo, hi, verbose=0):
        "returns the intersection between self and interval [lo, hi[ relative to this interval"
        if lo == None: lo = -1e300
        if hi == None: hi = +1e300
        if hi <= lo: return 0.0
        surface = 0.0
        # est-ce que la modalité est inversée ?
        if self.maxSupport < self.minSupport:
            # compter la zone ]-inf, maxCore]
            l = min(lo, self.maxCore)
            h = min(hi, self.maxCore)
            if l < h:
                k = 1.0
                surface += k * (h-l)
            # compter la zone ]maxCore, maxSupport[
            l = max(lo, self.maxCore)
            h = min(hi, self.maxSupport)
            if l < h:
                mul = self.getMu(l)
                muh = self.getMu(h)
                k = muh + 0.5*(mul-muh)
                surface += k * (h-l)
            # compter la zone ]minSupport, minCore[
            l = max(lo, self.minSupport)
            h = min(hi, self.minCore)
            if l < h:
                mul = self.getMu(l)
                muh = self.getMu(h)
                k = mul + 0.5*(muh-mul)
                surface += k * (h-l)
            # compter la zone [minCore, +inf[
            l = max(lo, self.minCore)
            h = max(hi, self.minCore)
            if l < h:
                k = 1.0
                surface += k * (h-l)
        else:
            # compter la zone ]minSupport, minCore[
            l = max(lo, self.minSupport)
            h = min(hi, self.minCore)
            if l < h:
                mul = self.getMu(l)
                muh = self.getMu(h)
                k = mul + 0.5*(muh-mul)
                surface += k * (h-l)
            # compter la zone [minCore, maxCore]
            l = max(lo, self.minCore)
            h = min(hi, self.maxCore)
            if l < h:
                k = 1.0
                surface += k * (h-l)
            # compter la zone ]maxCore, maxSupport[
            l = max(lo, self.maxCore)
            h = min(hi, self.maxSupport)
            if l < h:
                mul = self.getMu(l)
                muh = self.getMu(h)
                k = muh + 0.5*(mul-muh)
                surface += k * (h-l)
        # résultat final
        result = surface / (hi - lo)
        if verbose:
            print(self.modname, lo, hi, "=>", result)
        return result

    def getMinAlphaCut(self, alpha):
        "returns the lower bound of alpha-cut"
        return (self.minCore - self.minSupport)*alpha + self.minSupport

    def getMaxAlphaCut(self, alpha):
        "returns the upper bound of alpha-cut"
        return (self.maxCore - self.maxSupport)*alpha + self.maxSupport

    def __str__(self):
        return "Modality %s ]%.1f,[%.1f,%.1f],%.1f["%(self.modname, self.minSupport, self.minCore, self.maxCore, self.maxSupport)



class EnumModality(Modality):
    "This class represents a modality of an attribute, ex: 'reliable' for attribute 'carBrands' represented by a enumeration of weighted values"
    
    def isTrapeziumModality(self):
        return False
    def isEnumModality(self):
        return True
    
    def __init__(self, modname, enumeration):
        Modality.__init__(self, modname)
        self.enumeration = enumeration

    def getDerivedPredicate(self, alpha=0):
        ret= " IN ("
        for k in self.enumeration.keys():
            if self.enumeration.get(k) >= alpha:
                ret+="'"+(k.replace("'","''"))+"',"
        return ret[:-1]+")"

    def getMu(self, v):
        "returns the satisfaction degree of v to this modality"
        v = str(v).strip()
        ret= self.enumeration.get(v, 0.0)
        return ret

    def __str__(self):
        s = str(self.enumeration)
        if len(s) > 30:
            s = s[:30]+"...}"
        return "Modality %s %s"%(self.modname, s)


## tests de cette classe
#if __name__ == "__main__":
#    m1 = TrapeziumModality("weekend", 5,5,7,7)
#    print m1
#    print m1.getMu(7)


class Partition:
    "This class represents the partition of an attribute with several modalities, ex: 'age' = { 'young', 'medium', 'old' }" 
    def __init__(self, attname):
        ""
        self.attname = attname
        self.modalities = dict()
        self.modnames = list()
        self.nbModalitites = 0

    def getModNames(self):
        return self.modnames

    def isTrapeziumPartition(self):
        return all(m.isTrapeziumModality() for m in self.modalities.values())
    def isEnumPartition(self):
        return all(m.isEnumModality() for m in self.modalities.values())

    def addTrapeziumModality(self, modname, minSupport, minCore, maxCore, maxSupport):
        "add a trapezium modality to this partition"
        if modname in self.modalities:
            raise Exception("Partition %s: already defined modality %s"%(self.attname, modname))
        self.modalities[modname] = TrapeziumModality(modname, minSupport, minCore, maxCore, maxSupport)
        self.modnames.append(modname)
        self.nbModalitites += 1

    def addEnumModality(self, modname, enumeration):
        "add a enumeration modality to this partition"
        if modname in self.modalities:
            raise Exception("Partition %s: already defined modality %s"%(self.attname, modname))
        self.modalities[modname] = EnumModality(modname, enumeration)
        self.modnames.append(modname)
        self.nbModalitites += 1

    def getAttName(self):
        "returns the name of this partition, its attribute identifier"
        return self.attname

    def getModalities(self):
        "returns an iterator on its modalities"
        for modname in self.modnames:
            yield self.modalities[modname]

    def getLabels(self):
        return OrderedDict(self.modalities).keys()

    def getNbModalities(self):
        return self.nbModalitites

    def getModality(self, modname):
        "return the specified modality, exception if absent"
        return self.modalities[modname]

    def __str__(self):
        return "Partition %s:\n\t\t"%self.attname + "\n\t\t".join(map(lambda n: str(self.modalities[n]), self.modnames))

    def __repr__(self):
        return self.__str__()



class Vocabulary:
    "This class represents a fuzzy vocabulary"

    def __init__(self, filename):
        self.nbParts = 0
        "reads a CSV file whose format is : attname,modname,minSupport,minCore,maxCore,maxSupport"
        # dictionary of the partitions
        self.partitions = dict()
        self.attributeNames = list()
        self.mappingTab=None


        with open(filename, 'r') as source:
            for line in source:
                line = line.strip()

                if line == "" or line[0] == "#": 
                    if self.mappingTab is None:
                        "We consider that the first line is the list of attribute names"
                        self.mappingTab = dict()
                        atts = line[1:].split(',')
                        self.fields = atts
                        for a in range(len(atts)):
                            self.mappingTab[atts[a]] = a

                else:
                    words = line.split(',')
                    if len(words) == 6:
                        # modalité de type trapèze
                        attname,modname,minSupport,minCore,maxCore,maxSupport = words
                        # update existing partition or create new one if missing
                        partition = self.partitions.setdefault(attname, Partition(attname))
                        partition.addTrapeziumModality(modname, float(minSupport), float(minCore), float(maxCore), float(maxSupport))
                    elif len(words) == 3:
                        # modalité de type énuméré
                        attname,modname,enumeration = words
                        # analyser l'enumération en tant que dictionnaire {valeur:poids}
                        enumeration = enumeration.split(';')
                        enumeration = map(lambda vw: (vw.split(':')[0], float(vw.split(':')[1])), enumeration)
                        enumeration = dict(enumeration)
                        # update existing partition or create new one if missing
                        partition = self.partitions.setdefault(attname, Partition(attname))
                        partition.addEnumModality(modname, enumeration)
                    else:
                        raise Exception("%s: bad format line %s"%(filename, line))
        self.attributeNames = self.partitions.keys()

    def getFields(self):
        return self.fields

    def getAttributeNames(self):
        return self.attributeNames

    def getNbPartitions(self):
        return self.nbParts

    def getPartitions(self):
        return self.partitions.values()

    def getDescribedAttributes(self):
        return OrderedDict(self.partitions).keys()

    def getPartition(self, attname):
        return self.partitions[attname]

    def __str__(self):
        return "Vocabulary:\n\t" + "\n\t".join(map(str, self.partitions.values()))

    def __repr__(self):
        return self.__str__()

    def mapping(self, a):
        if a not in self.mappingTab.keys():
            raise Exception("Attribute %s not found in the vocabulary (mapping)"%(a))
        return self.mappingTab[a]
                    

if __name__ == '__main__':
    vocFile='FlightsVoc2.txt'
    #vocFile='/Users/smits/Data/Research/Prototypes/HistogramBasedLinguisticSummarization/Data/cars.voc'
    v = Vocabulary(vocFile)
    print(v)

