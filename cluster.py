import csv
import wals
import operator
from sklearn.cluster import KMeans

if __name__ == "__main__":
    langs,X = wals.getLangFeatures("language.csv", 0.6)

    km = KMeans(n_clusters = 20)

    km.fit(X)
    
    print km.labels_

    with open("langclusters.txt", "w") as out:
        langlab = sorted(zip(langs, km.labels_), key=operator.itemgetter(1))
    
        for lang,lab in langlab:
            out.write(str(lab) + "\t" + lang + "\n")
    
    cc = km.cluster_centers_
    ll = km.labels_

