## WALS Scripts


This is a set of scripts to play with WALS. I'm interested in finding language similarity and language clusters using WALS features.

I'm particularly interested in using phonological features for the purpose of transliteration. These are features 1-19. 

See a demo of langsim.py at http://104.131.29.154:1234/langsim

Notice that the WALS data comes from wals.info, and the following license must be attached.

### WALS Online data download


Data of WALS Online is published under the following license:
http://creativecommons.org/licenses/by/4.0/

It should be cited as

Dryer, Matthew S. & Haspelmath, Martin (eds.) 2013.
The World Atlas of Language Structures Online.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://wals.info, Accessed on 2015-07-30.)


## UPSID Data

I also downloaded UPSID data from http://www.linguistics.ucla.edu/faciliti/sales/software.htm

This data is in upsid_matrix.tsv

There are 919 segments. Not every line has 919 fields (they may truncate a little early).

If a non-space element shows up in a certain index, then only that element will ever appear in that index. (Verified experimentally). This means that the matrix is essentially a bit-vector (it might be valuable to pay special attention to sounds (or classes of sounds) that have interpretation, such as consonants and vowels).

See this page for info: http://web.phonetik.uni-frankfurt.de/upsid_info.html