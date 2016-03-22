#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Biopython官方文档中实例演示，以备查询。
"""

#序列的创建于输出
print("\n###############\n1. 简单序列处理\n---------------")
from Bio.Seq import Seq
my_seq = Seq("AGTACACTGGT") #创建Seq()
print("my_seq:", my_seq)    #输出
print(repr(my_seq)) #原始输出
print("alphabet of my_seq:", my_seq.alphabet)   #序列类型

#互补
print("正向互补:", my_seq.complement())
print("反向互补:", my_seq.reverse_complement())

#外部导入序列
print("\n###############\n2. FASTA 解析示例\n---------------")
from Bio import SeqIO
for seq_record in SeqIO.parse("ls_orchid.fasta", "fasta"):  #解析fasta文件
    print("序列名称:", seq_record.id)
    print("序列原始输出:", repr(seq_record.seq))
    print("序列长度:", len(seq_record))
    break
#FASTA 文件并没有指定字母表，因此默认使用相当通用的 SingleLetterAlphabet()

print("\n###############\n3. GenBank 解析示例\n---------------")
for seq_record in SeqIO.parse("ls_orchid.gbk", "genbank"):  #解析genbank文件
    print("序列名称:", seq_record.id)
    print("序列原始输出:", repr(seq_record.seq))
    print("序列长度:", len(seq_record))
    break
#GenBank文件能够选择一个合理的字母表

#序列和字母表：Bio.Alphabet模块
print("\n###############\n4. 序列和字母表\n---------------")
print("序列字母表:", my_seq.alphabet)
from Bio.Alphabet import IUPAC
#指定字母表
my_seq = Seq("AGTACACTGGT", IUPAC.unambiguous_dna)  #明确DNA序列
print("序列字母表:", my_seq.alphabet)
my_prot = Seq("AGTACACTGGT", IUPAC.protein) #氨基酸序列
print("序列字母表:", my_prot.alphabet)

#序列的字符串性质
print("序列的迭代：")
for index, letter in enumerate(my_seq):
    print(index, letter)
print("序列长度:", len(my_seq))
print("序列索引:", my_seq[-1])
print("序列切片:", my_seq[4:8])
#获取下面 DNA 序列密码子第一、第二、第三位的碱基
print("序列切片1st:", my_seq[0::3])
print("序列切片2nd:", my_seq[1::3])
print("序列切片3rd:", my_seq[2::3])
print("序列反转:", my_seq[::-1])

print("非重叠计数:(AC)", my_seq.count("AC"))
print("GC含量:", 100 * float(my_seq.count("G") + my_seq.count("C")) / len(my_seq))

from Bio.SeqUtils import GC
print("GC含量:",GC(my_seq))
# Bio.SeqUtils.GC() 函数时会自动处理序列和可代表 G 或者 C 的歧意核苷酸字母 S 混合的情况。

#Seq()对象转换为字符串
print(str(my_seq))
fasta_format_string = ">Name\n%s\n" % my_seq
print(fasta_format_string)
#print(my_seq.tostring())

#序列连接
protein_seq = Seq("EVRNAK", IUPAC.protein)
dna_seq = Seq("ACGT", IUPAC.unambiguous_dna)
try:
    print(protein_seq + dna_seq)
except:
    print("字母表不兼容，连接失败！")

#字母表转换为兼容类型
from Bio.Alphabet import generic_alphabet
protein_seq.alphabet = generic_alphabet
dna_seq.alphabet = generic_alphabet
try:
    print(protein_seq + "--" + dna_seq)
    print("字母表兼容，连接成功！")
except:
    print("字母表不兼容，连接失败！")

#连接后字母表的变化
from Bio.Alphabet import generic_nucleotide
nuc_seq = Seq("GATCGATGC", generic_nucleotide)
dna_seq = Seq("ACGT", IUPAC.unambiguous_dna)

print(nuc_seq.alphabet, "+", dna_seq.alphabet, "=", (nuc_seq + dna_seq).alphabet)

#大小写更改
from Bio.Alphabet import generic_dna
dna_seq = Seq("acgtACGT", generic_dna)
print("原始序列:", dna_seq)
print("大写序列:", dna_seq.upper())
print("小写序列:", dna_seq.lower())

#转录
print("\n###############\n5. 转录/逆转录\n---------------")
coding_dna = Seq("ATGGCCATTGTAATGGGCCGCTGAAAGGGTGCCCGATAG", IUPAC.unambiguous_dna)
print("编码链DNA:", coding_dna)
template_dna = coding_dna.reverse_complement()
print("模板链DNA:", template_dna)
messenger_rna = coding_dna.transcribe()
print("     mRNA:", messenger_rna, messenger_rna.alphabet)

#从模板链去做一个真正的生物学上的转录，需要两步：
print(" 真实步骤:", template_dna.reverse_complement().transcribe())

#mRNA 逆向转录为 DNA 编码链
print("   逆转录:", messenger_rna.back_transcribe())

#翻译
print("\n###############\n6. 翻译\n---------------")
print("mRNA翻译:", repr(messenger_rna.translate()))
print("coding DNA翻译:", repr(coding_dna.translate()))
#指定密码子表名
print("线粒体遗传密码表翻译:", repr(coding_dna.translate(table="Vertebrate Mitochondrial")))
#指定NCBI 上表格的标号
print("线粒体遗传密码表翻译:", repr(coding_dna.translate(table=2)))
#提前终止翻译
print("coding DNA翻译终止:", repr(coding_dna.translate(to_stop=True)))
#指定终止符
print("指定终止符:", repr(coding_dna.translate(table=2, stop_symbol="@")))
#完整CDS翻译，E. coli K12 yaaX基因, 非标准的起始密码子
gene = Seq("GTGAAAAAGATGCAATCTATCGTACTCGCACTTTCCCTGGTTCTGGTCGCTCCCATGGCA" + \
    "GCACAGGCTGCGGAAATTACGTTAGTCCCGTCAGTAAAATTACAGATAGGCGATCGTGAT" + \
    "AATCGTGGCTATTACTGGGATGGAGGTCACTGGCGCGACCACGGCTGGTGGAAACAACAT" + \
    "TATGAATGGCGAGGCAATCGCTGGCACCTACACGGACCGCCGCCACCGCCGCGCCACCAT" + \
    "AAGAAAGCTCCTCATGATCATCACGGCGGTCATGGTCCAGGCAAACATCACCGCTAA",generic_dna)
print("CDS翻译1:", repr(gene.translate(table="Bacterial")))
print("CDS翻译2:", repr(gene.translate(table="Bacterial", to_stop=True)))
"""
在细菌遗传密码中 GTG 是个有效的起始密码子。正常情况下编码缬氨酸，如果作为起始密码子，则翻
译成甲硫氨酸。当你告诉 Biopython 你的序列是完整 CDS 时，这事将会发生。
"""
print("完整CDS翻译:", repr(gene.translate(table="Bacterial", cds=True)))

#密码子表
from Bio.Data import CodonTable
standard_table = CodonTable.unambiguous_dna_by_name["Standard"]
mito_table = CodonTable.unambiguous_dna_by_name["Vertebrate Mitochondrial"]
#或者
standard_table = CodonTable.unambiguous_dna_by_id[1]
mito_table = CodonTable.unambiguous_dna_by_id[2]
print("标准密码子表:\n" + standard_table)
print("线粒体密码子表:\n" + mito_table)
#终止/起始密码子
print("线粒体密码子表终止密码子:", mito_table.stop_codons)
print("线粒体密码子表起始密码子:", mito_table.start_codons)

#比较 Seq 对象
print("\n###############\n7. 比较Seq对象\n---------------")
seq1 = Seq("ACGT", IUPAC.unambiguous_dna)
seq2 = Seq("ACGT", IUPAC.unambiguous_dna)
if seq1 == seq2:
    print("seq1 == seq2")
else:
    print("seq1 != seq2")
if id(seq1) == id(seq2):
    print("id(seq1) == id(seq2)")
else:
    print("id(seq1) != id(seq2)")
if str(seq1) == str(seq2):
    print("str(seq1) == str(seq2)")
else:
    print("str(seq1) != str(seq2)")

#MutableSeq 对象
"""
就像正常的 Python 字符串，Seq 对象是“只读的”，在 Python 术语上就是不可变的。除了想要 Seq 对
象表现得向一个字符串之外，这是一个很有用的默认，因为在生物学应用上你往往需要确保你没有改动你的
序列数据
"""
print("\n###############\n8. 可变对象\n---------------")
my_seq = Seq("GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA", IUPAC.unambiguous_dna)
try:
    my_seq[5] = "G"
    print("可以改变碱基")
except:
    print("无法改变碱基")
mutable_seq = my_seq.tomutable() #转换为可变对象
print("可变对象(转变):", repr(mutable_seq))
from Bio.Seq import MutableSeq
mutable_seq = MutableSeq("GCCATTGTAATGGGCCGCTGAAAGGGTGCCCGA", IUPAC.unambiguous_dna) #直接创建可变对象
print("可变对象(创建):", repr(mutable_seq))
try:
    mutable_seq[5] = "C"
    print("可以改变碱基")
except:
    print("无法改变碱基")

#转换为只读对象
new_seq = mutable_seq.toseq()
