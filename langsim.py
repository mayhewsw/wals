
import argparse
import cluster
from scipy.spatial.distance import cosine 
import csv

def getlangs(fname):
    langs = []
    with open(fname) as csvfile:
        f = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in f:
            if i == 0:
                header = line
                i += 1
                continue

            langs.append(line[3])
    return langs

    
def langsim(fname, lang, threshold, phon, only_hr=False, topk=10, comp=False):
    langs,X = cluster.getLangFeatures(fname, threshold, phon)

    # get HR languages here
    hrthreshold = 1000
    if only_hr:
        hrlangs = set()
        with open("/home/venv/projects/projects/wals/filesizes.txt") as fs:
            for line in fs:
                sline = line.strip().split()
                if int(sline[0]) > hrthreshold:
                    langname = sline[1].split(".")[1]
                    hrlangs.add(langname)
    
    #print "Returned {0} languages".format(len(langs))

    tl = ""
    for l in langs:
        if l[3] == lang:
            tl = l
            
        if comp and (l[3] == lang or l[3] == comp):
            print l[3] + "\t" + str(cluster.mp(l[10:]))

    if comp:
        exit()

    if tl == "":
        return [(-1, "Language '{0}' not found...".format(lang))]

    # get feats for tl
    mtl = cluster.mp(tl[10:])

    dists = []

    for l in langs:
        if l[3] == lang:
            continue
        if only_hr and l[3].split()[0] not in hrlangs:
            continue
        t = cluster.mp(l[10:])
        dists.append((cosine(t,mtl), ",".join([l[3],l[6],l[7],l[8]])))

    dists = sorted(dists)

    return dists[:topk]
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lang")
    parser.add_argument("threshold", type=float)
    parser.add_argument("--phon", help="use phonology features only", action="store_true")
    parser.add_argument("--topk", help="show top k results", type=int, default=10)
    parser.add_argument("--comp", help="compare lang with this lang")
    parser.add_argument("--highresource", help="only compare with high resource", action="store_true")
    
    args = parser.parse_args()

    print "lang: ",args.lang
    print "threshold: ", args.threshold

    print langsim("language.csv", args.lang, args.threshold, phon=args.phon, topk=args.topk, comp=args.comp, only_hr=args.highresource)
    
