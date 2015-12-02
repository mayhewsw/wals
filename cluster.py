#!/usr/bin/python

from sklearn.cluster import KMeans
import csv

def mp(x):
    out = []
    for v in x:
        if len(v) == 0:
            out.append(0)
        else:
            out.append(int(v[0]))
    return out

def getLangFeatures(frac = 0.0, phon=False):
    """ This returns only those languages with frac of the features non-zero."""
    with open("language.csv") as csvfile:
        f = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        i = 0
        X = []
        langs = []
        for line in f:
            if i == 0:
                header = line
                #print "Header len is: ", len(header)
                i += 1
                continue

            if phon:
                m = mp(line[10:39])
                sline = line[:39]
            else:
                m = mp(line[10:])
                sline = line

            bools = map(lambda i: 1 if i > 0 else 0, m)

            if sum(bools) > frac*len(bools):
                X.append(m)
                langs.append(sline)
        return langs,X


if __name__ == "__main__":

    langs,X = getLangFeatures(0.6)
    
    km = KMeans(n_clusters = 20)

    km.fit(X)
    
    print km.labels_

    import operator
    

    with open("langclusters.txt", "w") as out:
        langlab = sorted(zip(langs, km.labels_), key=operator.itemgetter(1))
    
        for lang,lab in langlab:
            out.write(str(lab) + "\t" + lang + "\n")
    
    cc = km.cluster_centers_
    ll = km.labels_

