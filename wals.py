import csv
import numpy as np

# Phonology index range (strict python indexing)
PHON_INDS = (0,19)

# Morphology index range (strict python indexing)
MORPH_INDS = (19,31)


class WALSLanguage:
    """
    This represents a single language in the WALS system. This contains a feature
    vector for the WALS features.
    """

    def mp(self, x):
        """
        This turns the WALS vector into an integer vector. Each feature
        has the format: <int> <Description>.
        This just returns the int.
        """
        out = []
        for v in x:
            if len(v) == 0:
                out.append(0)
            else:
                out.append(int(v[0]))
        return out

    def __init__(self, header, walslist):
        # Is this high resource language?
        self.hr = False

        # Store everything
        self.dctzip = zip(header, walslist)
        self.dct = dict(self.dctzip)

        # WALS feats
        self.feats = self.mp(walslist[10:])

        # lat and long
        self.coords = (walslist[4], walslist[5])

        # percentage of items that are nonzero
        self.nonzerofrac = np.count_nonzero(self.phon_feats()) / float(len(self.phon_feats()))


    def __getitem__(self, item):
        return self.dct[item]

    def phon_feats(self):
        return self.feats[slice(*PHON_INDS)]

    def morph_feats(self):
        return self.feats[slice(*MORPH_INDS)]

    def __repr__(self):
        return "Language " + self.dct["Name"]

    def fullname(self):
        return self.dct["Name"] + ":" + self.dct["genus"] + ":" + self.dct["family"]

    def name(self):
        return self.dct["Name"]


def getHRLanguages(fname, hrthreshold=0):
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
    This loads the WALS file into the WALSLanguage data structures
    :param fname: name of WALS file, typically language.csv
    :return: list of WALSLanguage objects
    """

    import os
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    hrlangs = getHRLanguages(os.path.join(__location__, "langsizes.txt"))
        
    with open(fname) as csvfile:
        f = csv.reader(csvfile, delimiter=',', quotechar='"')
        langs = []

        header = f.next()
        # wals features begin at index 10
        maxvals = np.zeros(len(header[10:]))
        for line in f:
            lang = WALSLanguage(header, line)
            langs.append(lang)
            maxvals = np.maximum(maxvals, lang.feats)

            if lang["iso_code"] in hrlangs:
                lang.hr = True

        # normalize each feature by the maximum possible value.
        for lang in langs:
            lang.feats = lang.feats / maxvals

        langs = sorted(langs, key=lambda t: t.name().lower())
        return langs


if __name__ == "__main__":
    lf = loadLangs("language.csv")
    f = lf[8]