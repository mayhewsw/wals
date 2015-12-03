#!/usr/bin/python

import csv
import numpy as np
from scipy.sparse import csc_matrix

class UPSIDLanguage:
    """
    This represents a single language in the UPSID system. 
    """

    def __init__(self, tlist):
        # Is this high resource language?
        self.hr = False

        self.name = tlist[0].lower()

        # Known number
        self.NUMFEATS = 919

        self.feats = csc_matrix(self.mp(tlist[1:]))


    def mp(self, l):
        """
        Convert this list into a bit vector.
        """
        out = []
        for i in range(self.NUMFEATS):
            if i >= len(l) or l[i].strip() == "":
                out.append(0)
            else:
                out.append(1)
        return out

    def __repr__(self):
        return "Language " + self.name


def getHRLanguages(fname, hrthreshold=1000):
    """
    :param fname: the name of the file containing filesizes. Created using wc -l in the wikidata folder
    :param hrthreshold: how big a set of transliteration pairs needs to be considered high resource
    :return: a list of language names (in ISO 639-3 format?)
    """

    hrlangs = set()
    with open(fname) as fs:
        for line in fs:
            long,iso639_3,iso639_1,size = line.strip().split()
            if int(size) > hrthreshold:
                hrlangs.add(iso639_3)
    return hrlangs


def loadLangs(fname):
    """
    This loads the UPSID file into the UPSIDLanguage data structures
    :param fname: name of UPSID file, typically upsid_matrix.tsv
    :return: list of UPSIDLanguage objects
    """

    import os
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    hrlangs = getHRLanguages(os.path.join(__location__, "langsizes.txt"))
        
    with open(fname) as f:
        langs = []

        # wals features begin at index 10
        for line in f:
            lang = UPSIDLanguage(line.split("\t"))
            langs.append(lang)

            #if lang["iso_code"] in hrlangs:
            #    lang.hr = True

        return langs


def langsim(langname, langs):
    out = []

    # first get the language object
    tgtlang = None
    for lang in langs:
        if lang.name == langname:
            tgtlang = lang


    if tgtlang == None:
        print "Whops... didn't find " + langname
        return None

            
    for lang in langs:
        if tgtlang.name == lang.name:
            continue
        print lang.feats.shape
        print tgtlang.feats.shape
        # dot doesn't work???
        out.append((lang.feats.dot(tgtlang.feats), lang.name))
    return out

if __name__ == "__main__":
    lf = loadLangs("upsid_matrix.tsv")

    lst = langsim("french", lf)
    print lst
    
    
