#!/usr/bin/python

import argparse
import cluster
from scipy.spatial.distance import cosine 

parser = argparse.ArgumentParser()
parser.add_argument("lang")
parser.add_argument("threshold", type=float)
parser.add_argument("--phon", help="use phonology features only", action="store_true")
parser.add_argument("--topk", help="show top k results", type=int, default=10)
parser.add_argument("--comp", help="compare lang with this lang")

                    

args = parser.parse_args()

print "lang: ",args.lang
print "threshold: ", args.threshold

langs,X = cluster.getLangFeatures(args.threshold, args.phon)

print "Returned {0} languages".format(len(langs))

tl = ""
for l in langs:
    if l[3] == args.lang:
        tl = l

    if args.comp and (l[3] == args.lang or l[3] == args.comp):
        print l[3] + "\t" + str(cluster.mp(l[10:]))

if args.comp:
    exit()
    

if tl == "":
    print "Language '{0}' not found...".format(args.lang)
    exit()

# get feats for tl
mtl = cluster.mp(tl[10:])

dists = []

for l in langs:
    t = cluster.mp(l[10:])

    dists.append((cosine(t,mtl), ",".join([l[3],l[6],l[7],l[8]])))

dists = sorted(dists)
for i in range(args.topk):
    print dists[i]
    
    
