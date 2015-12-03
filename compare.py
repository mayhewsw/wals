import argparse
from scipy.spatial.distance import cosine
import wals


def compare(fname, lang1, lang2):
    """
    Given two language names, get distance according to phonology scores.
    :param fname: name of wals csv file
    :param lang1: name of first lang (eg English)
    :param lang2: name of second lang
    :return: the distance of the languages, or -1 if one or both langs not found.
    """

    langs = wals.loadLangs(fname)

    l1 = None
    l2 = None
    for lang in langs:
        if lang["Name"] == lang1:
            l1 = lang
        elif lang["Name"] == lang2:
            l2 = lang

    if l1 and l2:
        return cosine(l1.phon_feats(), l2.phon_feats())
    else:
        print "One or both langs not found: {0}, {1}".format(l1, l2)
        return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lang1")
    parser.add_argument("lang2")

    args = parser.parse_args()

    print "lang1: ", args.lang1
    print "lang2: ", args.lang2

    print compare("language.csv", args.lang1, args.lang2)