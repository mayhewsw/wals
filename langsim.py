import argparse
from scipy.spatial.distance import cosine 
import wals
import numpy as np


def langsim(fname, lang, threshold, phon, only_hr=False, topk=20):
    """
    Gets a topk list of languages similar to this language, various parameters control this.
    :param fname:
    :param lang:
    :param threshold:
    :param phon:
    :param only_hr:
    :param topk:
    :return:
    """
    langs = wals.loadLangs(fname)

    #langs = filter(lambda l: l.nonzerofrac > threshold, langs)

    tgtlang = None
    for l in langs:
        if l["iso_code"].decode("utf8") == lang:
            tgtlang = l
            break

    if tgtlang == None:
        return [(-1, "Language '{0}' not found...".format(lang.encode("utf8")))]

    # now filter by high resource
    # get tgtlang first, b/c it may not be high resource
    if only_hr:
        langs = filter(lambda l: l.hr, langs)

    dists = []

    tgtf = tgtlang.phon_feats()

    for l in langs:
        if l["iso_code"].decode("utf8") == lang:
            continue

        t = l.phon_feats()

        #dist = cosine(tgtf, t)
        numequal = sum(np.equal(tgtf, t))
        # now remove all places where they are both zero
        a = set(np.where(tgtf == 0)[0])
        b = set(np.where(t == 0)[0])

        numequal -= len(a.intersection(b))
        
        dist = 1 - numequal / float(len(tgtf))
        
        dists.append((dist, l.fullname()))

    dists = sorted(dists)

    return dists[:topk]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lang")
    parser.add_argument("threshold", type=float)
    parser.add_argument("--phon", help="use phonology features only", action="store_true")
    parser.add_argument("--topk", help="show top k results", type=int, default=10)
    parser.add_argument("--highresource", help="only compare with high resource", action="store_true")
    
    args = parser.parse_args()

    print "lang: ", args.lang
    print "threshold: ", args.threshold

    print langsim("language.csv", args.lang, args.threshold, phon=args.phon, topk=args.topk, only_hr=args.highresource)

    #print langsim("language.csv", "Hamtai", 0.7, True)
