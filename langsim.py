import argparse
from scipy.spatial.distance import cosine 
import wals





def langsim(fname, lang, threshold, phon, only_hr=False, topk=10):
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
    langs,X = wals.getLangFeatures(fname, threshold, phon)

    if only_hr:
        hrlangs = getHRLanguages("/home/venv/projects/projects/wals/filesizes.txt")
    else:
        hrlangs = set()

    tl = ""
    for l in langs:
        if l[3] == lang:
            tl = l

    if tl == "":
        return [(-1, "Language '{0}' not found...".format(lang))]

    # get feats for tl
    mtl = wals.mp(tl[10:])

    dists = []

    for l in langs:
        if l[3] == lang:
            continue
        if only_hr and l[3].split()[0] not in hrlangs:
            continue
        t = wals.mp(l[10:])
        dists.append((cosine(t,mtl), ",".join([l[3],l[6],l[7],l[8]])))

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

    print langsim("language.csv", args.lang, args.threshold, phon=args.phon, topk=args.topk, comp=args.comp, only_hr=args.highresource)
