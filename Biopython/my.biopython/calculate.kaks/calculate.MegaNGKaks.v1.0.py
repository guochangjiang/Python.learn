#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: calculate.MegaNGKaks.v1.0.py
       USAGE: $ python calculate.MegaNGKaks.v1.0.py -h
 DESCRIPTION: 使用MEGA中的NG法计算CDS序列的kaks值
     OPTIONS: -in cds.aln.fas -out kaks.csv
REQUIREMENTS: 比对好的coding DNA sequence且为3的整数倍长度
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/5/24 18:04:48
      UPDATE: 2016/5/24 18:04:48

 CHANGE LOGS:
     Version 1.0 2016/5/24 18:04:48    初始版本: 计算指定fasta文件的kaks值; 不支持二倍体简并碱基
'''

import argparse
import os
import re
import math

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-i",
                    "-in",
                    "--input",
                    metavar="input_file",
                    dest="fasta_in",
                    required=True,
                    type=str,
                    help="fasta file(align) to input")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="KaKs.MEGA_NG.csv",
                    type=str,
                    help="csv file to output, [default: KaKs.MEGA_NG.csv]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

#子例程
def get_Codon1_Codon2_syn_non_num_info():
    Codon1_Codon2_syn_non_num_info = {}
    for codon1 in Genetic_Codon2aa.keys():   #Stop Codon is not count, followed the rules of Mega4
        if codon1 in ("TAA", "TGA", "TAG"):
            continue
        Codon1_Codon2_syn_non_num_info[codon1] = {}
        for codon2 in Genetic_Codon2aa.keys():   #Stop Codon is not count, followed the rules of Mega4
            if codon2 in ("TAA", "TGA", "TAG"):
                continue
            Codon1_Codon2_syn_non_num_info[codon1][codon2] = []
            if codon1 != codon2:
                if get_diff_base_number(codon1, codon2) == 1:  # 2 Codon Diff 1
                    if Genetic_Codon2aa[codon1] == Genetic_Codon2aa[codon2]:
                        Codon1_Codon2_syn_non_num_info[codon1][codon2] = [1,0]
                    else:
                        Codon1_Codon2_syn_non_num_info[codon1][codon2] = [0,1]
                elif get_diff_base_number(codon1, codon2) == 2:  # 2 Codon Diff 1
                    intermediate_codons = get_intermediate_codon(codon1,codon2)
                    syn_way_number = 0
                    non_way_number = 0
                    for intermediate_codon in intermediate_codons:
                        if Genetic_Codon2aa[codon1] == Genetic_Codon2aa[intermediate_codon]:
                            syn_way_number += 1
                        elif Genetic_Codon2aa[codon1] != Genetic_Codon2aa[intermediate_codon]:
                            non_way_number += 1
                        if Genetic_Codon2aa[codon2] == Genetic_Codon2aa[intermediate_codon]:
                            syn_way_number += 1
                        elif Genetic_Codon2aa[codon2] != Genetic_Codon2aa[intermediate_codon]:
                            non_way_number += 1
                    syn_way_number_final = 0
                    non_way_number_final = 0
                    if syn_way_number + non_way_number != 0:
                        syn_way_number_final = 2 * syn_way_number / (syn_way_number + non_way_number)
                        non_way_number_final = 2 * non_way_number / (syn_way_number + non_way_number)
                    Codon1_Codon2_syn_non_num_info[codon1][codon2] = [syn_way_number_final,non_way_number_final]
                elif get_diff_base_number(codon1, codon2) == 3:  # 2 Codon Diff 1
                    intermediate_codons = get_intermediate_codon(codon1,codon2)
                    syn_way_number = 0
                    non_way_number = 0
                    empty_syn_and_non_number = 0
                    for intermediate_codon in intermediate_codons:  #AAA - 'BBB' - CCC - DDD
                        intermediate_codons_further = get_intermediate_codon(intermediate_codon,codon2)
                        for intermediate_codon_further in intermediate_codons_further: #AAA - BBB - 'CCC' - DDD
                            if Genetic_Codon2aa[codon1] == Genetic_Codon2aa[intermediate_codon]:
                                syn_way_number += 1
                            elif Genetic_Codon2aa[codon1] != Genetic_Codon2aa[intermediate_codon]:
                                non_way_number += 1
                            if Genetic_Codon2aa[intermediate_codon] == Genetic_Codon2aa[intermediate_codon_further]:
                                syn_way_number += 1
                            elif Genetic_Codon2aa[intermediate_codon] != Genetic_Codon2aa[intermediate_codon_further]:
                                non_way_number += 1
                            if Genetic_Codon2aa[codon2] == Genetic_Codon2aa[intermediate_codon_further]:
                                syn_way_number += 1
                            elif Genetic_Codon2aa[codon2] != Genetic_Codon2aa[intermediate_codon_further]:
                                non_way_number += 1
                    syn_way_number_final = 0
                    non_way_number_final = 0
                    if syn_way_number + non_way_number != 0:
                        syn_way_number_final = 3 * syn_way_number / (syn_way_number + non_way_number)
                        non_way_number_final = 3 * non_way_number / (syn_way_number + non_way_number)
                    Codon1_Codon2_syn_non_num_info[codon1][codon2] = [syn_way_number_final,non_way_number_final]
    return Codon1_Codon2_syn_non_num_info


#密码子中不同碱基数目
def get_diff_base_number(coden_1, codon_2):
    diff_num = 0
    for i in (0, 1, 2):
        if coden_1[i] != codon_2[i]:
            diff_num += 1
    return diff_num


#不同密码子的非终止组合（交换其中一个不同碱基）
def get_intermediate_codon(codon_1, codon_2):
    diff_num = 0
    my_dict = {}
    for i in (0, 1, 2):
        if codon_1[i] != codon_2[i]:
            my_dict[str(i)] = [codon_1[i], codon_2[i]]
    intermediate_codons = []
    for key in my_dict.keys():
        new_codon_1 = codon_1[0:int(key)] + my_dict[key][1] + codon_1[int(key)+1:]
        if new_codon_1 not in ("TAA", "TAG", "TGA"):
            intermediate_codons.append(new_codon_1)
    return intermediate_codons


#获取重叠序列
def OverLapCodon(seq1, seq2):
    ns1 = ''
    ns2 = ''
    codon_num=len(seq1)/3
    i=1
    while i <= codon_num:
        codon1=seq1[i*3-3:i*3]
        codon2=seq2[i*3-3:i*3]
        if re.search("[^ATCG]", codon1) or re.search("[^ATCG]", codon2):
            i += 1
        else:
            ns1 += codon1
            ns2 += codon2
            i += 1
    return (ns1,ns2)


def get_pn_ps(seq1, seq2):
    pN_num, pN_site1, pN_site2, pS_num, pS_site1, pS_site2 = 0,0,0,0,0,0
    align_len_seq1 = len(seq1)
    base1 = []
    base2 = []
    for i in range(align_len_seq1):
        base1.append(seq1[i])
        base2.append(seq2[i])
    triple_switch = 1
    codon1, codon2 = base1[0], base2[0]
    for i in range(align_len_seq1):
        b1 = base1[i]
        b2 = base2[i]
        if b1 != '-':
            if triple_switch < 3:
                codon1 += b1
                codon2 += b2
                triple_switch += 1
            if triple_switch == 3:
                print(codon1, '-', codon2)
                if Genetic_Codon2aa[codon1] and Genetic_Codon2aa[codon2] and Genetic_Codon2aa[codon1] != '_' and Genetic_Codon2aa[codon2] != '_':
                    codon1_non = Codon2Non_site[codon1]
                    codon1_syn = Codon2Syn_site[codon1]
                    codon2_non = Codon2Non_site[codon2]
                    codon2_syn = Codon2Syn_site[codon2]
                    pN_site1 += codon1_non
                    pN_site2 += codon2_non
                    pS_site1 += codon1_syn
                    pS_site2 += codon2_syn
                    pS_num_this_codon = 0
                    pN_num_this_codon = 0
                    if get_diff_base_number(codon1,codon2) == 0: # 0 base diff in codon
                        pass
                    elif get_diff_base_number(codon1,codon2) >= 1:
                        pS_num += Codon1_Codon2_syn_non_num_info[codon1][codon2][0]
                        pN_num += Codon1_Codon2_syn_non_num_info[codon1][codon2][1]
                codon1 = ''
                codon2 = ''
                triple_switch = 0
                print(pN_site1, pN_site2, pS_site1, pS_site2)
    pN_site = (pN_site1 + pN_site2) / 2
    pS_site = (pS_site1 + pS_site2) / 2
    return (pN_num, pN_site, pS_num, pS_site)


#全局变量
##Just a hash that link codon and aa
Genetic_Codon2aa = {
    'TCA': 'S',    # Serine
    'TCC': 'S',    # Serine
    'TCG': 'S',    # Serine
    'TCT': 'S',    # Serine
    'TTC': 'F',    # Phenylalanine
    'TTT': 'F',    # Phenylalanine
    'TTA': 'L',    # Leucine
    'TTG': 'L',    # Leucine
    'TAC': 'Y',    # Tyrosine
    'TAT': 'Y',    # Tyrosine
    'TAA': '_',    # Stop
    'TAG': '_',    # Stop
    'TGC': 'C',    # Cysteine
    'TGT': 'C',    # Cysteine
    'TGA': '_',    # Stop
    'TGG': 'W',    # Tryptophan
    'CTA': 'L',    # Leucine
    'CTC': 'L',    # Leucine
    'CTG': 'L',    # Leucine
    'CTT': 'L',    # Leucine
    'CCA': 'P',    # Proline
    'CCC': 'P',    # Proline
    'CCG': 'P',    # Proline
    'CCT': 'P',    # Proline
    'CAC': 'H',    # Histidine
    'CAT': 'H',    # Histidine
    'CAA': 'Q',    # Glutamine
    'CAG': 'Q',    # Glutamine
    'CGA': 'R',    # Arginine
    'CGC': 'R',    # Arginine
    'CGG': 'R',    # Arginine
    'CGT': 'R',    # Arginine
    'ATA': 'I',    # Isoleucine
    'ATC': 'I',    # Isoleucine
    'ATT': 'I',    # Isoleucine
    'ATG': 'M',    # Methionine
    'ACA': 'T',    # Threonine
    'ACC': 'T',    # Threonine
    'ACG': 'T',    # Threonine
    'ACT': 'T',    # Threonine
    'AAC': 'N',    # Asparagine
    'AAT': 'N',    # Asparagine
    'AAA': 'K',    # Lysine
    'AAG': 'K',    # Lysine
    'AGC': 'S',    # Serine
    'AGT': 'S',    # Serine
    'AGA': 'R',    # Arginine
    'AGG': 'R',    # Arginine
    'GTA': 'V',    # Valine
    'GTC': 'V',    # Valine
    'GTG': 'V',    # Valine
    'GTT': 'V',    # Valine
    'GCA': 'A',    # Alanine
    'GCC': 'A',    # Alanine
    'GCG': 'A',    # Alanine
    'GCT': 'A',    # Alanine
    'GAC': 'D',    # Aspartic Acid
    'GAT': 'D',    # Aspartic Acid
    'GAA': 'E',    # Glutamic Acid
    'GAG': 'E',    # Glutamic Acid
    'GGA': 'G',    # Glycine
    'GGC': 'G',    # Glycine
    'GGG': 'G',    # Glycine
    'GGT': 'G',    # Glycine
}

##################################################################################
##  This part is to get a hash that describes syn-site and non-site of each codon
##  The values of the hash were retrieved from Mega4
##################################################################################
Codon2Syn_site = {
    'AAA' : 1/3,
    'AAC' : 1/3,
    'AAG' : 1/3,
    'AAT' : 1/3,
    'ACA' : 1,
    'ACC' : 1,
    'ACG' : 1,
    'ACT' : 1,
    'AGA' : 5/6,
    'AGC' : 1/3,
    'AGG' : 2/3,
    'AGT' : 1/3,
    'ATA' : 2/3,
    'ATC' : 2/3,
    'ATG' : 0,
    'ATT' : 2/3,
    'CAA' : 1/3,
    'CAC' : 1/3,
    'CAG' : 1/3,
    'CAT' : 1/3,
    'CCA' : 1,
    'CCC' : 1,
    'CCG' : 1,
    'CCT' : 1,
    'CGA' : 3/2,
    'CGC' : 1,
    'CGG' : 4/3,
    'CGT' : 1,
    'CTA' : 4/3,
    'CTC' : 1,
    'CTG' : 4/3,
    'CTT' : 1,
    'GAA' : 1/3,
    'GAC' : 1/3,
    'GAG' : 1/3,
    'GAT' : 1/3,
    'GCA' : 1,
    'GCC' : 1,
    'GCG' : 1,
    'GCT' : 1,
    'GGA' : 1,
    'GGC' : 1,
    'GGG' : 1,
    'GGT' : 1,
    'GTA' : 1,
    'GTC' : 1,
    'GTG' : 1,
    'GTT' : 1,
    'TAC' : 1,
    'TAT' : 1,
    'TCA' : 1,
    'TCC' : 1,
    'TCG' : 1,
    'TCT' : 1,
    'TGC' : 1/2,
    'TGG' : 0,
    'TGT' : 1/2,
    'TTA' : 2/3,
    'TTC' : 1/3,
    'TTG' : 2/3,
    'TTT' : 1/3
}
Codon2Non_site = {}
for codon in Codon2Syn_site.keys():
    Codon2Non_site[codon] = 3 - Codon2Syn_site[codon]

##################################################################################
###  When codon1 => codon2, we count syn-num and non-num of each possibility
##################################################################################
Codon1_Codon2_syn_non_num_info = get_Codon1_Codon2_syn_non_num_info()

#主程序
OUT = open(args.file_out, "w")
for fasfile in(args.fasta_in,):
    print("do file:", fasfile, '......')
    result = []
    sum_all = 0
    sum_ka = 0
    sum_ks = 0
    ka = []
    ks = []
    sheep=0
    sheepy=0
    locus_list = []
    Allseq_dict = {}
    seq_name = ''
    with open(fasfile, 'r') as Data_in:
        for line in Data_in:
            line =  line.strip()
            if line == '':
                continue
            if line[0] == ">":
                seq_name = line[1:]
                if seq_name not in locus_list:
                    locus_list.append(seq_name)
                    Allseq_dict[seq_name] = ''
            else:
                Allseq_dict[seq_name] += line
    if locus_list == [] or len(locus_list) < 2:
        print("输入文件不合要求，请检查！")
        OUTPUT.write("#" + fasfile + ",-\n")
        os.exit(0)
    gene_num = len(locus_list)
    total_pair = gene_num * (gene_num -1) / 2
    process_pair = 1
    for i in range(len(locus_list)):
        first = Allseq_dict[locus_list[i]].upper()
        for j in range(i+1, len(locus_list)):
            print("Process rate: %d / %d\r" %(process_pair, total_pair), end = '')
            process_pair += 1
            second = Allseq_dict[locus_list[j]].upper()
            (first2,second2)=OverLapCodon(first,second)
            if re.search("^-+", first2) and re.search("^-+", second2):
                seq1=first2
                seq2=second2
                for i in range(len(seq1)):
                    if re.search("^-+", seq1) and re.search("^-+", seq2):
                        seq1 = seq1[1:]
                        seq2 = seq2[1:]
                    elif re.search("^-+", seq1) and not re.search("^-+", seq2):
                        seq1, seq2 = seq2, seq1
                    else:
                        break
            elif re.search("^-+", first2) and not re.search("^-+", second2):
                seq1 = second2
                seq2 = first2
            else:
                seq1=first2
                seq2=second2
            (pN_num, pN_site, pS_num, pS_site) = get_pn_ps(seq1, seq2)
            dN, dS = 0, 0
            if (1 - 4/3 * pN_num/pN_site) > 0 and (1 - 4/3 * pS_num/pS_site)>0:
                dN = 0 - 3/4 * math.log(1 - 4/3 * pN_num/pN_site)
                dS = 0 - 3/4 * math.log(1 - 4/3 * pS_num/pS_site)
            else:
                dN="N/C"
                dS="N/C"
            dNdS = ''
            if dN == "N/C" or dS == "N/C":
                dNdS = "N/C"
            elif dN==0 and dS==0:
                dNdS = '0/0'
                sheepy += 1
            elif dS ==0 and dN!=0:
                dNdS = 'N/0'
                sheepy += 1
                sum_ka += dN
            else:
                dNdS = dN /dS
                sum_all += dNdS
                sum_ka += dN
                sum_ks += dS
                sheep += 1
                sheepy += 1
            result.append(dNdS)
            ka.append(dN)
            ks.append(dS)
    average,ave_ka,ave_ks="","",""
    if sheep:
        average = sum_all / sheep
        ave_ks = sum_ks / sheepy
        ave_ka = sum_ka / sheepy
    OUT.write("#%s,average Ka/Ks=%s\n" %(fasfile, str(average)))
    for name in locus_list[1:]:
        OUT.write(",%s" %name)
    OUT.write("\n")
    for i in range(gene_num - 1):
        OUT.write(locus_list[i])
        OUT.write("%s" %(','*(i+1)))
        for j in range(gene_num - i - 1):
            OUT.write("%s," %str(result[j]))
            result = result[1:]
        OUT.write("\n")
    OUT.write("\n")
    OUT.write("#%s,average Ka=%s\n" %(fasfile, str(ave_ka)))
    for name in locus_list[1:]:
        OUT.write(",%s" %name)
    OUT.write("\n")
    for i in range(gene_num - 1):
        OUT.write(locus_list[i])
        OUT.write("%s" %(','*(i+1)))
        for j in range(gene_num - i - 1):
            OUT.write("%s," %str(ka[j]))
            ka = ka[1:]
        OUT.write("\n")
    OUT.write("\n")
    OUT.write("#%s,average Ks=%s\n" %(fasfile, str(ave_ks)))
    for name in locus_list[1:]:
        OUT.write(",%s" %name)
    OUT.write("\n")
    for i in range(gene_num - 1):
        OUT.write(locus_list[i])
        OUT.write("%s" %(','*(i+1)))
        for j in range(gene_num - i - 1):
            OUT.write("%s," %str(ks[j]))
            ks = ks[1:]
        OUT.write("\n")
    OUT.write("\n")
OUT.close()
