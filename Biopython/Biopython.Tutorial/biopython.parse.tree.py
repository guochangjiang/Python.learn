#!/usr/bin/env python3
#-*-coding: utf-8 -*-

from Bio import Phylo
tree = Phylo.read('example.tree.nwk', 'newick')
print(tree)
tree.ladderize()   # Flip branches so deeper clades are displayed at top
#Phylo.draw(tree)
Phylo.draw_ascii(tree)
Phylo.write(tree, 'example-both.xml', 'phyloxml')