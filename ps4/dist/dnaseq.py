#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = {}
        for pair in pairs:
            self.put(pair[0], pair[1])
    # Associates the value v with the key k.
    def put(self, k, v):
        if k in self.dict:
            self.dict[k].append(v)
        else:
            self.dict[k] = [v]
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k in self.dict:
            return self.dict[k]
        else:
            return []

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    current_word = ""
    i = 0
    while len(current_word) < k:
        current_word += next(seq)
    hash_str = RollingHash(current_word)
    for char in seq:
        yield [current_word, hash_str.current_hash(), i]
        hash_str.slide(current_word[0], char)
        i += 1
        current_word = current_word[1:] + char
        if len(current_word) < k:
            return

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    assert m>=k
    try:
        i = 0
        while True:
            current_word = ""
            while len(current_word) < k:
                current_word += next(seq)
            hash_str = RollingHash(current_word)
            yield [current_word, hash_str.current_hash(), i]
            for k in range(0, m-k):
                next(seq)
            i += m
    except StopIteration:
        return


# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    multidict_a = Multidict()
    for val in intervalSubsequenceHashes(a, k, m):
        multidict_a.put(val[1], (val[2], val[0]))
    for vals in subsequenceHashes(b, k):
        for apos, asubseq in multidict_a.get(vals[1]):
            if asubseq != vals[0]:
                continue
            yield (apos, vals[2])
    return

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
