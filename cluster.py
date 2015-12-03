
import csv

def mp(x):
    """ This turns the WALS vector into an integer vector. Each feature has the format: <int> <Description>.
    This just returns the int."""
    out = []
    for v in x:
        if len(v) == 0:
            out.append(0)
        else:
            out.append(int(v[0]))
    return out

PHON_INDS = (10,39)

def getLangFeatures(fname, frac = 0.0, phon=False):
    """ This returns only those languages with frac of the features non-zero."""
    with open(fname) as csvfile:
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
                m = mp(line[slice(*PHON_INDS)])
                sline = line[:PHON_INDS[1]]
            else:
                m = mp(line[10:])
                sline = line

            bools = map(lambda i: 1 if i > 0 else 0, m)

            if sum(bools) > frac*len(bools):
                X.append(m)
                langs.append(sline)
        return langs,X


if __name__ == "__main__":
    from sklearn.cluster import KMeans
    langs,X = getLangFeatures("language.csv", 0.6)

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

