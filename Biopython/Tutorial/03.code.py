#!/usr/bin/env python3
# --*-- utf-8 --*--

from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Alphabet import generic_dna

my_seq = Seq("AGTACACTGGT", IUPAC.unambiguous_dna)
my_seq
print(my_seq)
print(my_seq.alphabet)
print(my_seq.complement())
print(my_seq.reverse_complement())

my_seq2 = Seq("AGTACACTGGT", IUPAC.ambiguous_dna)
print(my_seq2.alphabet)
my_seq3 = Seq("AGTACACTGGT", IUPAC.extended_dna)
print(my_seq3.alphabet)

my_prot = Seq("AGTACACTGGT", IUPAC.protein)
print(my_prot)
print(my_prot.alphabet)

##seq object act like string
for index, letter in enumerate(my_seq):
    print("%i %s" % (index, letter))

print(len(my_seq))
print(my_seq[0]) #first letter
print(my_seq[-1]) #last letter

print(my_seq.count("AC"))

##GC content
print(100*float(my_seq.count("G")+my_seq.count("C"))/len(my_seq))

from Bio.SeqUtils import GC
print(GC(my_seq))


##Slicing a sequence
my_seq = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna)
print(my_seq[4:12])
print(my_seq[0::3])
print(my_seq[1::3])
print(my_seq[::-1]) #reverse
fasta_format_string = ">Name\n%s\n" % my_seq
print(fasta_format_string)

##连接
list_of_seqs = [Seq("ACGT", generic_dna), Seq("AACC", generic_dna), Seq("GGTT", generic_dna)]
concatenated = Seq("", generic_dna)
for s in list_of_seqs:
    concatenated += s
print(concatenated)
print(sum(list_of_seqs, Seq("", generic_dna)))

##changing case
dna_seq = Seq("acgtACGT", generic_dna)
print(dna_seq.upper())
print(dna_seq.lower())
print("GTAC" in dna_seq)
print("GTAC" in dna_seq.upper())

##互补序列
my_seq = Seq("GATCGATGGGCCTATATAGGATCGAAAATCGC", IUPAC.unambiguous_dna)
print(my_seq)
print(my_seq.complement())
print(my_seq.reverse_complement())

##转录
coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", IUPAC.unambiguous_dna)
messenger_rna = coding_dna.transcribe()
print(messenger_rna)
##反转录
print(messenger_rna.back_transcribe())

##翻译
coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", IUPAC.unambiguous_dna)
print(coding_dna.translate())
print(coding_dna.translate(table="Vertebrate Mitochondrial"))
print(coding_dna.translate(table=2))
print(coding_dna.translate(to_stop=True))
print(coding_dna.translate(table=2, to_stop=True))
print(coding_dna.translate(table=2, stop_symbol="@"))
gene = Seq("GTGAAAAAGATGCAATCTATCGTACTCGCACTTTCCCTGGTTCTGGTCGCTCCCATGGCA" +
    "GCACAGGCTGCGGAAATTACGTTAGTCCCGTCAGTAAAATTACAGATAGGCGATCGTGAT" +
    "AATCGTGGCTATTACTGGGATGGAGGTCACTGGCGCGACCACGGCTGGTGGAAACAACAT" +
    "TATGAATGGCGAGGCAATCGCTGGCACCTACACGGACCGCCGCCACCGCCGCGCCACCAT" +
    "AAGAAAGCTCCTCATGATCATCACGGCGGTCATGGTCCAGGCAAACATCACCGCTAA",
    generic_dna)

print(gene.translate(table="Bacterial"))
print(gene.translate(table="Bacterial", cds=True))

##查看密码子表
from Bio.Data import CodonTable
standard_table = CodonTable.unambiguous_dna_by_name["Standard"]
mito_table = CodonTable.unambiguous_dna_by_id[2]

print(standard_table)
print(mito_table.start_codons)
print(mito_table.stop_codons)
print(mito_table.forward_table["ACG"])

##可变对象
from Bio.Seq import MutableSeq
mutable_seq = MutableSeq("GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA", IUPAC.unambiguous_dna)
print(mutable_seq)
mutable_seq[5] = "C"
print(mutable_seq)
mutable_seq.remove("T")
print(mutable_seq)
mutable_seq.reverse()
print(mutable_seq)
new_seq = mutable_seq.toseq()
print(new_seq)
