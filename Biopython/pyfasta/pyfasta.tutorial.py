#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pyfasta

f = pyfasta.Fasta('three_chrs.fasta')
print(sorted(f.keys()))
print(f['chr1'])

# get full the sequence:
a = str(f['chr1'])
b = f['chr1'][:]
print(a)
print(b)

# get the 1st basepair in every codon (it's python yo)
print(f['chr1'][:10])
print(f['chr1'][::3])

# can query by a 'feature' dictionary (note this is one based coordinates)
print(f.sequence({'chr': 'chr1', 'start': 2, 'stop': 9}))
# same as:
print(f['chr1'][1:9])
# with reverse complement (automatic for - strand)
print(f.sequence({'chr': 'chr1', 'start': 2, 'stop': 9, 'strand': '-'}))

# use python, zero based coords
print(f.sequence({'chr': 'chr1', 'start': 2, 'stop': 9}, one_based=False))


#keyfunction
fkey = pyfasta.Fasta('key.fasta', key_fn=lambda key: key.split()[0])
print(sorted(fkey.keys()))

import numpy as np
a = np.array(f['chr2'])
