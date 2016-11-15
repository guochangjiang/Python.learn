#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: PythonPrimerDesign.v1.0.py
       USAGE: $ python PythonPrimerDesign.v1.0.py -h
 DESCRIPTION: 根据指定序列进行标准PCR引物设计
     OPTIONS: 
REQUIREMENTS: DNA sequence file(fasta)
        BUGS: -
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/6/13 20:07:56
      UPDATE: 2016/6/13 20:07:56

 CHANGE LOGS:
     Version 1.0 2016/6/13 20:07:56    初始版本:以 perlprimer v1.1.21 中 Standard PCR primer 程序为原型进行重新设计
'''

'''
用法举例：将引物设计参考序列存入Fasta文件，如dna.fasta， 在5'端100到200区域设计正向引物，3'端700到800设计反向引物。
         引物长度为20-24bp，Tm值在57℃ - 63℃之间，最大Tm差异为3℃，要求引物GC含量为40%-60%，要求引物末端3个碱基
         中至少有2个G/C（GC clamp), 要求引物单碱基重复数不多于4个，多碱基重复不多于3个，引物二聚体中匹配碱基不超过10个，
         而在3'可延伸二聚体中最后5个碱基不多于3个匹配碱基，把简略结果输出到dna.pyprimer.results.txt，且输出所有引物的详细信息，
         那么命令应为:
$ python PythonPrimerDesign.v1.0.py -in dna.fasta -range 100 200 700 800 -min_len 20 -max_len 24 \
                                    -min_tm 57 -max_tm 60 -max_tm_diff 3 -exclude_gc -min_gc 40 -max_gc 60 \
                                    -exclude_clamp -exclude_repeat_run -run 4 -repeat 3 \
                                    -exclude_max_dimer -max_dimer_bp 10 -exclude_max_3_dimer -max_3_dimer_bp 3/5 \
                                    --report -simple -out dna.pyprimer.results.txt
注意：如最后找到的引物数目为0，请根据输出中的过滤信息调整相应参数。
'''
import argparse
import re
import os
import math
import datetime

__version__ = '1.0'

#---------
# 子函数
#---------

# 清理序列中的空白字符与序列名行
def Clean_Sequence(sequence):
    sequence = re.sub("^\s*>(.*\n)", "", sequence)
    sequence = re.sub("[\s\n\r\d\-]", "", sequence)
    return sequence

# DNA互补序列
def Complement(DNA): 
    basecomplement ={
                    'A': 'T', 'a': 't', 'T': 'A', 't': 'a',
                    'G': 'C', 'g': 'c', 'C': "G", 'c': 'g',
                    'M': 'K', 'm': 'k', 'K': 'M', 'k': 'm',
                    'R': 'Y', 'r': 'y', 'Y': 'R', 'y': 'r',
                    'W': 'W', 'w': 'w', 'S': 'S', 's': 's',
                    'V': 'B', 'v': 'b', 'B': 'V', 'b': 'v',
                    'H': 'D', 'h': 'd', 'D': 'H', 'd': 'h',
                    'N': 'N', 'n': 'n', '-': '-', '*': '*',
                    }
    letters = list(DNA)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)

# 候选引物序列获取
def GetPrimerList(sequence, start, end, chain):
    global all_possible_forward_num
    global all_possible_reverse_num
    global GC_content_filter_forward_num
    global GC_content_filter_reverse_num
    global GC_clamp_filter_forward_num
    global GC_clamp_filter_reverse_num
    global run_filter_forward_num
    global run_filter_reverse_num
    global repeat_filter_forward_num
    global repeat_filter_reverse_num
    global tm_filter_forward_num
    global tm_filter_reverse_num
    subseq = sequence[start - 1:end]
    if chain == 0:
        subseq = Complement(subseq[::-1])
    subseq = subseq.upper()
    primer_list = []
    for i in range(len(subseq)):
        for primer_win in range(min_len, max_len+1):
            if i + primer_win > len(subseq): # 溢出判断
                continue
            currwindow = subseq[i:i+primer_win] # 当前oligo序列
            # 检查是否具有简并碱基
            if Check_Degenerate(currwindow):
                continue
            if chain:
                all_possible_forward_num += 1
            else:
                all_possible_reverse_num += 1
            # %GC过滤
            if exclude_gc:
                gc = GC_Content(currwindow)
                if gc < min_gc or gc > max_gc:
                    if chain:
                        GC_content_filter_forward_num += 1
                    else:
                        GC_content_filter_reverse_num += 1
                    continue
            # 3'端 GC夹过滤
            if exclude_gc_clamp:
                gc = GC_Content(currwindow[-3:])
                if gc < 50:
                    if chain:
                        GC_clamp_filter_forward_num += 1
                    else:
                        GC_clamp_filter_reverse_num += 1
                    continue
            # 重复碱基过滤
            if exclude_rr:
                # 重复单碱基过滤
                runfilter = "C{%d,}|A{%d,}|G{%d,}|T{%d,}" %(run, run, run, run)
                if re.search(runfilter, currwindow):
                    if chain:
                        run_filter_forward_num += 1
                    else:
                        run_filter_reverse_num += 1
                    continue
                # 重复多碱基过滤
                repeatfilter = "(.{2,})\1{%d,}" %(repeat - 1)
                if re.search(repeatfilter, currwindow):
                    if chain:
                        repeat_filter_forward_num += 1
                    else:
                        repeat_filter_reverse_num += 1
                    continue
            # Tm值过滤
            tm = Tm(currwindow)
            if min_tm <= tm[0] <= max_tm:
                if chain:
                    pos = i + start
                else:
                    pos = start + len(subseq) - i - primer_win
                primer_list.append([pos, primer_win, currwindow, tm[0]])
            else:
                if chain:
                    tm_filter_forward_num += 1
                else:
                    tm_filter_reverse_num += 1
    return primer_list

# 简并碱基检查
def Check_Degenerate(sequence):
    if re.search("[^ATGCatgc]", sequence):
        return 1
    else:
        return 0

# GC含量计算
def GC_Content(sequence):
    G_num = sequence.count('G')
    C_num = sequence.count('C')
    gc_content = (G_num + C_num) * 100 / len(sequence)
    return gc_content

# Tm值计算
def Tm(sequence):
    # Primer 3: Tm = 81.5 + 16.6(log10([Na+])) + .41*(%GC) - 600/length
    # 
    sequence = sequence.upper()
    seq_len = len(sequence)
    deltaH = deltaS = 0
    # 计算deltaH deltaS
    for i in range(seq_len - 1):
        nn = sequence[i:i+2]
        deltaH += oligo_dH[nn]
        deltaS += oligo_dS[nn]
    initterm = "init" + sequence[0]
    deltaH += oligo_dH[initterm]
    deltaS += oligo_dS[initterm]
    endterm = "init" + sequence[-1]
    deltaH += oligo_dH[endterm]
    deltaS += oligo_dS[endterm]
    salt_correction = 0
    if Mg_conc > dNTP_conc:
        salt_correction = math.sqrt(Mg_conc - dNTP_conc)
    Na_eq=(monovalent_cation_conc + 120 * salt_correction)/1000 # mM -> M
    deltaS += (0.368 * (seq_len - 1) * math.log(Na_eq))
    oligo_conc_mols = oligo_conc / 1000000000
    corrected_tm=((deltaH * 1000) / (deltaS + (1.987 * math.log(oligo_conc_mols/4)))) - 273.15
    deltaG = deltaH-((273.15 + temperature)*(deltaS/1000))
    return (corrected_tm, deltaH, deltaS, deltaG)

# 搜索Tm值匹配且引物二聚体符合要求的引物对
def Primer_Pair_Cal():
    primer_1_id = 0
    primer_count = 0
    global all_pp_num
    global tm_diff_filter_pp_num
    all_pp_num = len(primer_forward_list) * len(primer_reverse_list)
    for primer_1 in primer_forward_list:
        (primer_1_pos, primer_1_len, primer_1_seq, primer_1_tm) = primer_1
        primer_1_id += 1
        if primer_1_id not in primer_1_id_list:
                primer_1_id_list.append(primer_1_id)
                primer_1_bind_list.append([])
                primer_1_bind_list_full.append([])
        primer_2_id = 0
        for primer_2 in primer_reverse_list:
            (primer_2_pos, primer_2_len, primer_2_seq, primer_2_tm) = primer_2
            if primer_2_id not in primer_2_id_list:
                primer_2_id_list.append(primer_2_id)
                primer_2_bind_list.append([])
                primer_2_bind_list_full.append([])
            primer_2_id += 1
            primer_count += 1
            percent_process = primer_count * 100 / all_pp_num
            print("引物搜索进度: %2.0f%%\r" %percent_process, end='')
            amp_size = primer_2_pos - primer_1_pos + 1 + primer_2_len
            # Tm差值检查
            if abs(primer_1_tm - primer_2_tm) > max_tm_diff:
                tm_diff_filter_pp_num += 1
                continue
            # 引物二聚体分析
            primer_pairs_id_list.append([primer_1_id, primer_2_id]) # 记录正反向引物序号
            ## 1. 不考虑5'端二聚体
            primer_1_bind = []
            primer_dimer_score, primer_1_bind = Primer_Dimer(primer_1_seq, primer_1_seq, 1, '1')    # 正向引物二聚体
            if primer_1_bind_list[primer_1_id-1] == []:
                primer_1_bind_list[primer_1_id-1] = primer_1_bind
            primer_12_bind = []
            new_dimer_score, primer_12_bind= Primer_Dimer(primer_1_seq, primer_2_seq, 1, '12')        # 正/反 向引物二聚体
            primer_pairs_bind_list.append(primer_12_bind)
            if new_dimer_score < primer_dimer_score:
                primer_dimer_score = new_dimer_score
            primer_2_bind = []
            new_dimer_score, primer_2_bind= Primer_Dimer(primer_2_seq, primer_2_seq, 1, '2')        # 反向引物二聚体
            if primer_2_bind_list[primer_2_id-1] == []:
                primer_2_bind_list[primer_2_id-1] = primer_2_bind
            if new_dimer_score < primer_dimer_score:
                primer_dimer_score = new_dimer_score
            ## 2.考虑5'端二聚体
            primer_1_bind_full = []
            primer_dimer_score_full, primer_1_bind_full = Primer_Dimer(primer_1_seq, primer_1_seq, 0, '1')    # 正向引物二聚体
            if primer_1_bind_list_full[primer_1_id-1] == []:
                primer_1_bind_list_full[primer_1_id-1] = primer_1_bind_full
            primer_12_bind_full = []
            new_dimer_score, primer_12_bind_full = Primer_Dimer(primer_1_seq, primer_2_seq, 0, '12')        # 正/反 向引物二聚体
            primer_pairs_bind_list_full.append(primer_12_bind_full)
            if new_dimer_score < primer_dimer_score_full:
                primer_dimer_score_full = new_dimer_score
            primer_2_bind_full = []
            new_dimer_score, primer_2_bind_full = Primer_Dimer(primer_2_seq, primer_2_seq, 0, '2')        # 反向引物二聚体
            if primer_2_bind_list_full[primer_2_id-1] == []:
                primer_2_bind_list_full[primer_2_id-1] = primer_2_bind_full
            if new_dimer_score < primer_dimer_score_full:
                primer_dimer_score_full = new_dimer_score
            primer_pairs_list.append([primer_1_seq, primer_1_pos, primer_1_len, primer_1_tm, primer_2_seq, primer_2_pos, primer_2_len, primer_2_tm, amp_size, primer_dimer_score, primer_dimer_score_full, primer_1_id, primer_2_id])

# 引物二聚体计算
def Primer_Dimer(p1, p2, extenddimer, primer_flag):
    primer1_bases_dict = {}     # 引物1的反向碱基矩阵(1/0)
    primer2_base_compare = []   # 引物2的反向互补碱基矩阵(1/0)
    score = []
    primer_1_bind = []
    primer_2_bind = []
    primer_12_bind = []
    # 最大引物长度
    p1_len = len(p1)
    p2_len = len(p2)
    p_len = p1_len
    if p1_len < p2_len:
        p_len = p2_len
    p1_reverse = p1[::-1].lower()           # 第1条引物反向序列
    p2_reverse = p2[::-1].lower()           # 第2条引物反向序列
    p2_rev_com = Complement(p2_reverse)     # 第2条引物反向互补序列
    # 引物1碱基矩阵
    for base in ('a', 'g', 'c', 't'):
        primer1_bases_dict[base] = []
        for i in range(p1_len):
            primer1_bases_dict[base].append(0)
    for l in range(p1_len):
        base = p1_reverse[l]
        primer1_bases_dict[base][l]= 1
    # 引物2碱基矩阵
    for k in range(p2_len):
        primer2_base_compare.append(primer1_bases_dict[p2_rev_com[k]])
    primer_dimer_len = p1_len + p2_len - 1  # 考虑的引物二聚体的长度
    if extenddimer:
        primer_dimer_len = p_len - 1
    # 二聚体分析
    for k in range(primer_dimer_len):
        score.append(999)
        bind_str = ''
        score_p = 0
        # 忽略所有不可延伸的引物二聚体
        start = end = k
        if k > p1_len - 1:
            start = p1_len - 1
        if k > p2_len - 1:
            end = p2_len - 1
        if extenddimer and extend_dimer: # 判断正向引物3'端是否形成二聚体
            if primer2_base_compare[0][start] != 1:
                continue
            if primer2_base_compare[end][start-k] != 1:
                continue
        for l in range(p2_len):
            if (k - l) < p1_len:
                if k >= l:
                    bind_str += str(primer2_base_compare[l][k-l])
            else:
                bind_str += '2'
        if extenddimer:
            bind_str = re.sub("01(?=[^1])", "00", bind_str)
        if '1' not in bind_str:
            continue
        pb_init = None
        pb_end = 0
        for l in range(len(bind_str)):
            if bind_str[l] == '1':
                if pb_init == None:
                    pb_init = l
                pb_end = l
        if pb_init != None:
            for l in range(pb_init, pb_end):
                if bind_str[l:l+2] == "00":
                    continue
                if bind_str[l] == '2':
                    continue
                score_p += oligo_dG[p1[p1_len-k+l-1:p1_len-k+l+1] + p2_reverse.upper()[l:l+2]]
            initterm = "init" + p2_reverse.upper()[pb_init]
            score_p += oligo_dG[initterm]
            endterm = "init" + p2_reverse.upper()[pb_end]
            score_p += oligo_dG[endterm]
            score[k] = float("%.2f" %score_p)
            if primer_flag == '1':
                primer_1_bind.append([k, score[k], bind_str, p1])
            if primer_flag == '2':
                primer_2_bind.append([k, score[k], bind_str, p2])
            if primer_flag == '12':
                primer_12_bind.append([k, score[k], bind_str, p1, p2])
            #dimer_align_str = Dimer_Align(p1, p2, k, bind_str)
            #print("K:%d bind: %s" %(k, bind_str))
            #print(dimer_align_str)
    if primer_flag == '1':
        return (sorted(score)[0], primer_1_bind)
    elif primer_flag == '2':
        return (sorted(score)[0], primer_2_bind)
    elif primer_flag == '12':
        return (sorted(score)[0], primer_12_bind)
    else:
        return sorted(score)[0]

# 获取oligo_dG
def recalculate_dG():
    salt_correction = 0
    if Mg_conc > dNTP_conc:
        salt_correction = math.sqrt(Mg_conc - dNTP_conc)
    Na_eq=(monovalent_cation_conc + 120 * salt_correction)/1000 # mM -> M
    entropy_adjust = (0.368 * math.log(Na_eq))
    for key in oligo_dH_full:
        if 'init' in key:
            continue
        dS = oligo_dS_full[key] + entropy_adjust
        dG = oligo_dH_full[key] - ((273.15 + 25) * (dS / 1000))
        oligo_dG[key] = dG

# 根据获取的二聚体信息生成对齐的二聚体字符串
def Dimer_Align(p1, p2, k, bind):
    p1 = p1.upper()
    p2 = p2.upper()[::-1]
    align_str = ''
    if k < len(p1):
        align_str += ("5' %s 3'\n" %p1)
        align_str += " " * (len(p1) + 2 - k)
        for b in bind:
            if b == '1':
                align_str += '|'
            else:
                align_str += '.'
        align_str += "\n"
        align_str += " " * (len(p1) - 1 - k)
        align_str += ("3' %s 5'\n" %p2)
    else:
        align_str += " " * (k+1-len(p1))
        align_str += ("5' %s 3'\n" %p1)
        #align_str += " " * (k+4-len(p1))
        align_str += " " * 3
        for b in bind:
            if b == '1':
                align_str += '|'
            else:
                align_str += '.'
        align_str += "\n"
        align_str += ("3' %s 5'\n" %p2)
    return align_str


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
                    help="序列所在fasta文件")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="tmp.pyprimer.txt",
                    type=str,
                    help="输出文件 [默认: tmp.pyprimer.txt]")
parser.add_argument(
                    "-min_tm",
                    "--minimum_Tm_of_primer",
                    metavar="minimum_Tm_of_primer",
                    dest="min_tm",
                    default=57,
                    type=int,
                    help="引物最小Tm值(℃)[默认:57]")
parser.add_argument(
                    "-max_tm",
                    "--maximum_Tm_of_primer",
                    metavar="maximum_Tm_of_primer",
                    dest="max_tm",
                    default=63,
                    type=int,
                    help="引物最大Tm值(℃)[默认:63]")
parser.add_argument(
                    "-max_tm_diff",
                    "--max_tm_diff",
                    metavar="maximum_difference_between_Tm_of_primers",
                    dest="max_tm_diff",
                    default=3,
                    type=int,
                    help="正反向引物间Tm值最大差值(℃)[默认:3]")
parser.add_argument(
                    "-min_len",
                    "--minimum_length_of_primer",
                    metavar="minimum_length_of_primer",
                    dest="min_len",
                    default=20,
                    type=int,
                    help="引物最小长度(bp)[默认:20]")
parser.add_argument(
                    "-max_len",
                    "--maximum_length_of_primer",
                    metavar="maximum_length_of_primer",
                    dest="max_len",
                    default=24,
                    type=int,
                    help="引物最大长度(bp)[默认:24]")
parser.add_argument(
                    '-range',
                    "--amplified_range",
                    nargs=4,
                    dest="region",
                    required=True,
                    type=int,
                    help='指定正反向引物的设计范围, 例如 100 200 900 1000')
parser.add_argument(
                    '-exclude_gc',
                    "--exclude_primer_with_abnormal_gc",
                    action='store_true',
                    default=False,
                    dest='exclude_gc',
                    help='过滤GC含量不在指定范围的引物')
parser.add_argument(
                    "-min_gc",
                    "--minimum_gc_of_primer",
                    metavar="minimum_gc_of_primer",
                    dest="min_gc",
                    default=40,
                    type=int,
                    help="引物GC含量最小值(%%)[默认:40]")
parser.add_argument(
                    "-max_gc",
                    "--maximum_gc_of_primer",
                    metavar="maximum_gc_of_primer",
                    dest="max_gc",
                    default=60,
                    type=int,
                    help="引物GC含量最大值(%%)[默认:60]")
parser.add_argument(
                    '-exclude_clamp',
                    "--exclude_primer_without_gc_clamp",
                    action='store_true',
                    default=False,
                    dest='exclude_gc_clamp',
                    help="过滤不含3'帽子的引物(3'端的3个碱基至少2个为G/C)")
parser.add_argument(
                    '-exclude_repeat_run',
                    "--exclude_primer_with_repeat_and_run",
                    action='store_true',
                    default=False,
                    dest='exclude_rr',
                    help="排除单/多碱基重复超过指定值的引物")
parser.add_argument(
                    "-run",
                    "--number_consecutive_bases_exclude",
                    metavar="number_consecutive_bases_exclude",
                    dest="run",
                    default=4,
                    type=int,
                    help="引物中单碱基重复的最大数目[默认:4]")
parser.add_argument(
                    "-repeat",
                    "--number_repeat_bases_exclude",
                    metavar="number_repeat_bases_exclude",
                    dest="repeat",
                    default=3,
                    type=int,
                    help="引物中多碱基重复的最大数目[默认:3]")
parser.add_argument(
                    '-remain_extend_dimer',
                    "--remain_extend_primer_dimer",
                    action='store_true',
                    default=False,
                    dest='remain_extend_dimer',
                    help="保留形成可延伸3'端二聚体的引物(对)")
parser.add_argument(
                    '-exclude_max_dimer',
                    "--exclude_primer_with_max_dimer_basepair_num",
                    action='store_true',
                    default=False,
                    dest='exclude_max_dimer',
                    help="排除引物中二聚体匹配碱基数超过指定数目的引物")
parser.add_argument(
                    "-max_dimer_bp",
                    "--max_dimer_basepair_num",
                    metavar="maxinum_number_of_dimer_basepair",
                    dest="max_dimer_bp",
                    default=5,
                    type=int,
                    help="引物中二聚体匹配碱基最大数目[默认:5]")
parser.add_argument(
                    '-exclude_max_3_dimer',
                    "--exclude_primer_with_max_3_dimer_basepair_num",
                    action='store_true',
                    default=False,
                    dest='exclude_max_3_dimer',
                    help="排除引物中3'端二聚体匹配碱基数超过指定数目的引物")
parser.add_argument(
                    "-max_3_dimer_bp",
                    "--max_3_dimer_basepair_num",
                    metavar="maxinum_number_of_3'_dimer_basepair",
                    dest="max_3_dimer_bp",
                    default='3/5',
                    type=str,
                    help="引物中3'端二聚体N个碱基匹配最大数目(n/m: 3'端m个碱基中最多3个匹配)[默认:3/5]")
parser.add_argument(
                    '-r',
                    "--report",
                    action='store_true',
                    default=False,
                    dest='report_out',
                    help="引物详细信息输出")
parser.add_argument(
                    '-simple',
                    "--simple_out",
                    action='store_true',
                    default=False,
                    dest='simple_out',
                    help="引物信息简略输出")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="本程序的版本号.",
                    version="版本号: " + __version__)
args = parser.parse_args()

#参数读取
min_tm = args.min_tm                            # 引物最小Tm值
max_tm = args.max_tm                            # 引物最大Tm值
max_tm_diff = args.max_tm_diff                  # 引物Tm值最大差异
min_len = args.min_len                          # 引物最小长度
max_len = args.max_len                          # 引物最大长度
(min_range_5p, min_range_3p,
max_range_5p, max_range_3p) = args.region       # 引物设计的前后范围
exclude_gc = args.exclude_gc                    # 是否排除GC含量超出范围的引物
min_gc = args.min_gc                            # 引物最小GC含量
max_gc = args.max_gc                            # 引物最大GC含量
exclude_gc_clamp = args.exclude_gc_clamp        # 是否要求引物最后3个碱基中至少具有2个G/C
exclude_rr = args.exclude_rr                    # 是否排除repeats/runs
run = args.run                                  # 重复单碱基(>=run)过滤
repeat = args.repeat                            # 重复多碱基(>=repeat)过滤
extend_dimer = not args.remain_extend_dimer     # 是否过滤可延伸引物二聚体
exclude_max_dimer = args.exclude_max_dimer      # 排除引物中二聚体匹配碱基数超过指定数目的引物
max_dimer_basepair_num = args.max_dimer_bp      # 引物中二聚体匹配碱基最大数目
exclude_max_3_dimer = args.exclude_max_3_dimer  # 排除引物中3'端二聚体匹配碱基数超过指定数目的引物
max_3_dimer_basepair_num = args.max_3_dimer_bp  # 引物中3'端二聚体N个碱基匹配最大数目
max_3_dimer_total_num = 0                       # 引物中3'端二聚体N个碱基
max_3_dimer_bp_num = 0                          # 引物中3'端二聚体碱基匹配最大数目
report_out = args.report_out                # 输出详细结果

m = re.match("(\d+)/(\d+)", max_3_dimer_basepair_num)
if m:
    max_3_dimer_total_num = int(m.group(2))
    max_3_dimer_bp_num = int(m.group(1))

# PCR反应条件
oligo_conc = 200                            # 引物浓度(nM)
Mg_conc = 1.5                               # 离子浓度(mM)
monovalent_cation_conc = 50                 # 一价阳离子,一般是钾离子浓度(mM)
dNTP_conc = 0.2                             # dNTP浓度(mM)

# 温度
temperature = 25                            # 计算引物二聚体ΔG时的温度


# 全局变量
oligo_dH = { # NN parameters in 1M NaCl pH 7 at 37°C
        "AA": -7.9, "TT": -7.9,
        "AT": -7.2, "TA": -7.2,
        "CA": -8.5, "TG": -8.5,
        "GT": -8.4, "AC": -8.4,
        "CT": -7.8, "AG": -7.8,
        "GA": -8.2, "TC": -8.2,
        "CG": -10.6, "GC": -9.8,
        "GG": -8.0, "CC": -8.0,
        "initC": 0.1, "initG": 0.1,
        "initA": 2.3, "initT": 2.3
        }
oligo_dH_full = {
        "AATT": -7.9, "TTAA": -7.9, 
        "ATTA": -7.2, "TAAT": -7.2, 
        "CAGT": -8.5, "TGAC": -8.5, 
        "GTCA": -8.4, "ACTG": -8.4, 
        "CTGA": -7.8, "AGTC": -7.8, 
        "GACT": -8.2, "TCAG": -8.2, 
        "CGGC": -10.6, "GCCG": -9.8, 
        "GGCC": -8.0, "CCGG": -8.0,

        "initC": 0.1, "initG": 0.1, 
        "initA": 2.3, "initT": 2.3, 
        # Like pair mismatches
        "AATA": 1.2, "ATAA": 1.2,
        "CAGA": -0.9, "AGAC": -0.9,
        "GACA": -2.9, "ACAG": -2.9,
        "TAAA": 4.7, "AAAT": 4.7, 
        
        "ACTC": 0.0, "CTCA": 0.0, 
        "CCGC": -1.5, "CGCC": -1.5,
        "GCCC": 3.6, "CCCG": 3.6, 
        "TCAC": 6.1, "CACT": 6.1, 
        
        "AGTG": -3.1, "GTGA": -3.1,
        "CGGG": -4.9, "GGGC": -4.9,
        "GGCG": -6.0, "GCGG": -6.0,
        "TGAG": 1.6, "GAGT": 1.6, 
        
        "ATTT": -2.7, "TTTA": -2.7,
        "CTGT": -5.0, "TGTC": -5.0,
        "GTCT": -2.2, "TCTG": -2.2,
        "TTAT": 0.2, "TATT": 0.2, 
        # G.T mismatches
        "AGTT": 1.0,  "TTGA": 1.0,
        "ATTG":  -2.5, "GTTA":  -2.5,
        "CGGT":  -4.1, "TGGC":  -4.1,
        "CTGG":  -2.8, "GGTC":  -2.8,
        "GGCT":  3.3, "TCGG":  3.3,
        "GGTT":  5.8, "TTGG":  5.8,
        "GTCG":  -4.4, "GCTG":  -4.4,
        "GTTG":  4.1, "GTTG":  4.1,
        "TGAT":  -0.1, "TAGT":  -0.1,
        "TGGT":  -1.4, "TGGT":  -1.4,
        "TTAG":  -1.3, "GATT":  -1.3,
        # G.A: mismatches
        "AATG":  -0.6, "GTAA":  -0.6,
        "AGTA":  -0.7, "ATGA":  -0.7,
        "CAGG":  -0.7, "GGAC":  -0.7,
        "CGGA":  -4.0, "AGGC":  -4.0,
        "GACG":  -0.6, "GCAG":  -0.6,
        "GGCA":  0.5, "ACGG":  0.5,
        "TAAG":  0.7, "GAAT":  0.7,
        "TGAA":  3.0, "AAGT":  3.0,
        # C.T mismatches
        "ACTT":  0.7, "TTCA":  0.7,
        "ATTC":  -1.2, "CTTA":  -1.2,
        "CCGT":  -0.8, "TGCC":  -0.8,
        "CTGC":  -1.5, "CGTC":  -1.5,
        "GCCT":  2.3, "TCCG":  2.3,
        "GTCC":  5.2, "CCTG":  5.2,
        "TCAT":  1.2, "TACT":  1.2,
        "TTAC":  1.0, "CATT":  1.0,
        # A.C mismatches
        "AATC":  2.3,"CTAA":  2.3,
        "ACTA":  5.3, "ATCA":  5.3, 
        "CAGC":  1.9, "CGAC":  1.9, 
        "CCGA":  0.6, "AGCC":  0.6, 
        "GACC":  5.2, "CCAG":  5.2, 
        "GCCA":  -0.7, "ACCG":  -0.7,
        "TAAC":  3.4,  "CAAT":  3.4, 
        "TCAA":  7.6, "AACT":  7.6,
        }

oligo_dS = { # NN parameters in 1M NaCl pH 7 at 37°C
        "AA": -22.2, "TT": -22.2, 
        "AT": -20.4, "TA": -21.3, 
        "CA": -22.7, "TG": -22.7, 
        "GT": -22.4, "AC": -22.4, 
        "CT": -21.0, "AG": -21.0, 
        "GA": -22.2, "TC": -22.2, 
        "CG": -27.2, "GC": -24.4, 
        "GG": -19.9, "CC": -19.9, 
        "initC": -2.8, "initG": -2.8, 
        "initA": 4.1, "initT": 4.1, 
        "sym": -1.4
    }

oligo_dS_full={
        "AATT": -22.2, "TTAA": -22.2, 
        "ATTA": -20.4, "TAAT": -21.3, 
        "CAGT": -22.7, "TGAC": -22.7, 
        "GTCA": -22.4, "ACTG": -22.4, 
        "CTGA": -21.0, "AGTC": -21.0, 
        "GACT": -22.2, "TCAG": -22.2, 
        "CGGC": -27.2, "GCCG": -24.4, 
        "GGCC": -19.9, "CCGG": -19.9,
        "initC": -2.8, "initG": -2.8, 
        "initA":  4.1, "initT": 4.1,
        "sym": -1.4,
        # Like pair mismatches
        "AATA":  1.7, "ATAA": 1.7,
        "CAGA": -4.2, "AGAC": -4.2, 
        "GACA": -9.8, "ACAG": -9.8, 
        "TAAA": 12.9, "AAAT": 12.9, 
        "ACTC": -4.4, "CTCA": -4.4, 
        "CCGC": -7.2, "CGCC": -7.2, 
        "GCCC":  8.9, "CCCG": 8.9, 
        "TCAC": 16.4, "CACT": 16.4, 
        "AGTG": -9.5, "GTGA": -9.5, 
        "CGGG": -15.3, "GGGC": -15.3,
        "GGCG": -15.8, "GCGG": -15.8,
        "TGAG":  3.6,  "GAGT": 3.6, 
        "ATTT": -10.8, "TTTA": -10.8,
        "CTGT": -15.8, "TGTC": -15.8,
        "GTCT": -8.4, "TCTG": -8.4, 
        "TTAT": -1.5, "TATT": -1.5,
        # G.T mismatches
        "AGTT":  0.9,  "TTGA": 0.9,
        "ATTG":  -8.3, "GTTA":  -8.3,
        "CGGT":  -11.7, "TGGC":  -11.7,
        "CTGG":   -8.0, "GGTC":  -8.0,
        "GGCT":   10.4, "TCGG":  10.4,
        "GGTT":   16.3, "TTGG":  16.3,
        "GTCG":  -12.3, "GCTG":  -12.3,
        "GTTG":    9.5, "GTTG":  9.5,
        "TGAT":   -1.7, "TAGT":  -1.7,
        "TGGT":   -6.2, "TGGT":  -6.2,
        "TTAG":   -5.3, "GATT":  -5.3, 
        # G.A mismatches
        "AATG":  -2.3, "GTAA":  -2.3,
        "AGTA":  -2.3, "ATGA":  -2.3,
        "CAGG":  -2.3, "GGAC":  -2.3,
        "CGGA":  -13.2, "AGGC":  -13.2,
        "GACG":  -1.0, "GCAG":  -1.0,
        "GGCA":  3.2, "ACGG":  3.2,
        "TAAG":  0.7, "GAAT":  0.7,
        "TGAA":  7.4, "AAGT":  7.4, 
        # C.T mismatches
        "ACTT":  0.2, "TTCA":  0.2,
        "ATTC":  -6.2, "CTTA":  -6.2,
        "CCGT":  -4.5, "TGCC":  -4.5,
        "CTGC":  -6.1, "CGTC":  -6.1,
        "GCCT":  5.4, "TCCG":  5.4, 
        "GTCC":  13.5, "CCTG":  13.5,
        "TCAT":  0.7, "TACT":  0.7, 
        "TTAC":  0.7, "CATT":  0.7, 
        # A.C mismatches
        "AATC":  4.6, "CTAA":  4.6,
        "ACTA":  14.6, "ATCA":  14.6,
        "CAGC":  3.7, "CGAC":  3.7, 
        "CCGA":  -0.6, "AGCC":  -0.6,
        "GACC":  14.2, "CCAG":  14.2,
        "GCCA":  -3.8, "ACCG":  -3.8,
        "TAAC":  8.0,  "CAAT":  8.0, 
        "TCAA":  20.2, "AACT":  20.2,
        }

oligo_dG = {  # NN parameters in 1M NaCl pH 7 at 37°C
        "AA": -1.00, "TT": -1.00, 
        "AT": -0.88, "TA": -0.58, 
        "CA": -1.45, "TG": -1.48, 
        "GT": -1.44, "AC": -1.44, 
        "CT": -1.28, "AG": -1.28, 
        "GA": -1.30, "TC": -1.30, 
        "CG": -2.17, "GC": -2.24, 
        "GG": -1.84, "CC": -1.84, 
        "initC": 0.98, "initG": 0.98, 
        "initA": 1.03, "initT": 1.03,}
recalculate_dG()

# 变量声明
DNA_seq = ""                                # DNA序列
max_ampsize = max_range_3p - min_range_5p   # 最大延伸长度
primer_forward_list = []                    # 正向候选引物信息列表(位置, 长度, 序列, Tm值)
primer_reverse_list = []                    # 反向候选引物信息列表(位置, 长度, 序列, Tm值)
primer_pairs_list = []                      # 符合要求的引物对信息列表: 0-3. 正向引物序列、位置、长度、Tm; 
                                                                      # 4-7: 反向引物序列、位置、长度、Tm;
                                                                      # 8. 扩展长度; 
                                                                      # 9. 引物二聚体(可延伸)最大deltaG值; 
                                                                      # 10. 引物二聚体(不可延伸)最大deltaG值; 
                                                                      # 11. 正向引号序号; 12.反向引物序号
primer_pairs_id_list = []                   # 符合要求的引物对序号[正向引物序号，反向引物序号]
primer_pairs_bind_list = []                 # 符合要求的引物对二聚体相关信息([k, deltaG, bind_str, p1, p2])
primer_pairs_bind_list_full = []            # 符合要求的引物对二聚体相关信息(包含5'端二聚体)([k, deltaG, bind_str, p1, p2])
primer_1_id_list = []                       # 符合要求的正向引物对序号
primer_1_bind_list = []                     # 符合要求的正向引物二聚体相关信息([k, deltaG, bind_str, p1])
primer_1_bind_list_full = []                # 符合要求的正向引物二聚体相关信息(包含5'端二聚体)([k, deltaG, bind_str, p1])
primer_2_id_list = []                       # 符合要求的反向引物对序号
primer_2_bind_list = []                     # 符合要求的反向引物二聚体相关信息([k, deltaG, bind_str, p2])
primer_2_bind_list_full = []                # 符合要求的反向引物二聚体相关信息(包含5'端二聚体)([k, deltaG, bind_str, p2])
all_possible_forward_num = 0                # 所有可能的正向引物序列
all_possible_reverse_num = 0                # 所有可能的反向引物序列
GC_content_filter_forward_num = 0           # 正向引物中被GC含量过滤掉的数目
GC_content_filter_reverse_num = 0           # 反向引物中被GC含量过滤掉的数目
GC_clamp_filter_forward_num = 0             # 正向引物中被GC帽子含量过滤掉的数目
GC_clamp_filter_reverse_num = 0             # 反向引物中被GC帽子含量过滤掉的数目
run_filter_forward_num = 0                  # 正向引物中被单碱基重复过滤掉的数目
run_filter_reverse_num = 0                  # 反向引物中被单碱基重复过滤掉的数目
repeat_filter_forward_num = 0               # 正向引物中被多碱基重复过滤掉的数目
repeat_filter_reverse_num = 0               # 反向引物中被多碱基重复过滤掉的数目
tm_filter_forward_num = 0                   # 正向引物中被Tm值过滤掉的数目
tm_filter_reverse_num = 0                   # 反向引物中被Tm值过滤掉的数目
all_pp_num = 0                              # 候选引物对数目
tm_diff_filter_pp_num = 0                   # 候选引物对中被Tm差值过滤掉的数目
max_dimer_filter_forward_num = 0            # 候选引物对正向引物被二聚体匹配碱基数过滤掉的数目
max_dimer_filter_reverse_num = 0            # 候选引物对反向引物被二聚体匹配碱基数过滤掉的数目
max_3_dimer_filter_forward_num = 0          # 候选引物对正向引物被3'端二聚体匹配碱基数过滤掉的数目
max_3_dimer_filter_reverse_num = 0          # 候选引物对反向引物被3'端二聚体匹配碱基数过滤掉的数目
max_dimer_filter_pp_num = 0                 # 候选引物对被二聚体匹配碱基数过滤掉的数目
max_3_dimer_filter_pp_num = 0               # 候选引物对被3'端二聚体匹配碱基数过滤掉的数目



#读取序列
print("读取序列中 ...")
with open(args.fasta_in) as IN:
    for line in IN:
        DNA_seq += line
DNA_seq = Clean_Sequence(DNA_seq)
#DNA_seq = DNA_seq.upper()
# 空序列检查
if len(DNA_seq) == 0:
    print("No DNA sequence found1")
    os.exit(0)
# 范围检查
if min_range_5p >= min_range_3p or max_range_5p >= max_range_3p or min_range_3p >= max_range_5p or max_range_3p > len(DNA_seq):
    print("ERROR amplified range!")
    os.exit(0)
# 互补序列获取
DNA_seq_reverse = DNA_seq[::-1]
DNA_seq_reverse_complement = Complement(DNA_seq_reverse)

# 候选正向引物获取
print("候选引物获取 ...")
primer_forward_list = GetPrimerList(DNA_seq, min_range_5p, min_range_3p, 1) # 1 means forward
primer_reverse_list = GetPrimerList(DNA_seq, max_range_5p, max_range_3p, 0) # 0 means reverse

# 搜索Tm值匹配且引物二聚体符合要求的引物对
print("搜索符合条件的引物 ...")
Primer_Pair_Cal()

# 输出结果
print("\n搜索完成，共获得引物对数目为: %d" %(len(primer_pairs_list)))
OUT = open(args.file_out, 'w')
if report_out:
    REPORT = open(args.file_out+".report", 'w')
# 获取当前时间
now = datetime.datetime.now()
time_detail = now.strftime('%Y-%m-%d %H:%M:%S')
# 文件头生成
OUT.write("# Result generated at %s\n" %time_detail)
if report_out:
    OUT.write("# See file %s for more info\n" %(args.file_out+".report"))
OUT.write('# fasta file: %s\n' %args.fasta_in)
# 过滤条件生成
OUT.write("#\n# filter conditions\n")
OUT.write("#-Primer Tm range: %d ℃ - %d ℃\n" %(min_tm, max_tm))
OUT.write("#-Max Tm difference: %d ℃\n" %max_tm_diff)
OUT.write("#-Primer length range: %d bp - %d bp\n" %(min_len, max_len))
OUT.write("#-Amplicon range: 5' %d - %d  3' %d - %d\n" %(min_range_5p, min_range_3p, max_range_5p, max_range_3p))
if exclude_gc:
    OUT.write("#-GC content: %d %% - %d %%\n" %(min_gc, max_gc))
if exclude_gc_clamp:
    OUT.write("#-GC clamp(two of the last three bases G or C)\n")
if exclude_rr:
    OUT.write("#-single base repeat: %d\n" %run)
    OUT.write("#-two or more bases repeat: %d\n" %repeat)
if args.remain_extend_dimer:
    OUT.write("#-remain primer with 3' extensible dimer\n")
if exclude_max_dimer:
    OUT.write("#-exclude primer with dimer more than %d complementary bases\n" %max_dimer_basepair_num)
if exclude_max_3_dimer:
    OUT.write("#-exclude primer with %d bp 3' dimer with more than %d bp complementary bases\n" %(max_3_dimer_total_num, max_3_dimer_bp_num))
if report_out:
    REPORT.write("# Report generated at %s\n" %time_detail)
    REPORT.write("# See file %s simple result\n" %(args.file_out))
    REPORT.write('# fasta file: %s\n' %args.fasta_in)

if not args.simple_out:
    out_str = '\n----------------\nALL PRIMER PAIRS\n----------------\n\n'
else:
    OUT.write("\n#Foward_Primer\tPos\tLen\tTm\tReverse_Primer\tPos\tTm\tAmp_size\tExt_dimer_dG\tFull_dimer_dG\n")
if report_out:
    report_str = '\n引物详情(未考虑二聚体情况)\n--------------------------\n'

primer_pair_total_num = len(primer_pairs_list)
primer_pair_num = 0     # 符合条件的引物对数
pp_id = 0
# 最佳引物筛选
if not args.simple_out:
    best_pp_str = "\n-----------------------------------------\nBest Primer Pair(only 3'-dimer concerned)\n"
    best_pp_dG_extand = -999
    best_pp_dG_full = -999
    for primer_info in primer_pairs_list:
        pp_id += 1
        if best_pp_dG_extand < primer_info[9]:
            best_pp_dG_extand = primer_info[9]
        if best_pp_dG_full < primer_info[10]:
            best_pp_dG_full = primer_info[10]
        (p1_id, p2_id) = primer_info[-2:]
        p_dG_list = []
        p_dG_list_full = []
        for p_bind_info in primer_1_bind_list[p1_id-1]:
            p_dG_list.append(p_bind_info[1])
        for p_bind_info in primer_1_bind_list_full[p1_id-1]:
            p_dG_list_full.append(p_bind_info[1])
        for p_bind_info in primer_2_bind_list[p2_id-1]:
            p_dG_list.append(p_bind_info[1])
        for p_bind_info in primer_2_bind_list_full[p2_id-1]:
            p_dG_list_full.append(p_bind_info[1])
        for p_bind_info in primer_pairs_bind_list[pp_id-1]:
            p_dG_list.append(p_bind_info[1])
        for p_bind_info in primer_pairs_bind_list_full[pp_id-1]:
            p_dG_list_full.append(p_bind_info[1])
        if p_dG_list:
            min_p_dG = min(p_dG_list)
            if best_pp_dG_extand < min_p_dG and min_p_dG != 999:
                best_pp_dG_extand = min_p_dG
        if p_dG_list_full:
            min_p_dG = min(p_dG_list_full)
            if best_pp_dG_full < min_p_dG and min_p_dG != 999:
                best_pp_dG_full = min_p_dG
    best_pp_str += (" 3' -dimer ΔG: %.2f\n" %best_pp_dG_extand)
    best_pp_str += ("full dimer ΔG: %.2f\n" %best_pp_dG_full)

pp_id = 0
foward_primer_filter_by_dimer=[]
foward_primer_filter_by_3_dimer=[]
reverse_primer_filter_by_dimer=[]
reverse_primer_filter_by_3_dimer=[]
for primer_info in primer_pairs_list:
    pp_id += 1
    process_rate = (pp_id) * 100 / primer_pair_total_num
    print("引物过滤中 %3.0f %% ...\r" %process_rate, end='')
    (p1_id, p2_id) = primer_info[-2:]
    # 所有二聚体中ΔG最小值序号
    max_dG_id_p1 = 0
    max_dG_id_p2 = 0
    max_dG_id_pp = 0
    # 所有可延伸的二聚体中ΔG最小值序号
    max_dG_id_p1_extend = 0
    max_dG_id_p2_extend = 0
    max_dG_id_pp_extend = 0
    # 所有二聚体中匹配碱基数最大值序号
    max_dimer_id_p1 = 0
    max_dimer_id_p2 = 0
    max_dimer_id_pp = 0
    # 所有可延伸的二聚体中匹配碱基数最大值序号
    max_dimer_id_p1_extend = 0
    max_dimer_id_p2_extend = 0
    max_dimer_id_pp_extend = 0
    p1_bind_str_list = primer_1_bind_list[p1_id-1]
    p1_bind_str_list_full = primer_1_bind_list_full[p1_id-1]
    if len(p1_bind_str_list_full) == 0:
        continue
    p2_bind_str_list = primer_2_bind_list[p2_id-1]
    p2_bind_str_list_full = primer_2_bind_list_full[p2_id-1]
    if len(p2_bind_str_list_full) == 0:
        continue
    pp_bind_str_list = primer_pairs_bind_list[pp_id-1]
    pp_bind_str_list_full = primer_pairs_bind_list_full[pp_id-1]
    p_dG_list = []
    p_dG_list_full = []
    for p_bind_info in primer_1_bind_list[p1_id-1]:
        p_dG_list.append(p_bind_info[1])
    for p_bind_info in primer_1_bind_list_full[p1_id-1]:
        p_dG_list_full.append(p_bind_info[1])
    for p_bind_info in primer_2_bind_list[p2_id-1]:
        p_dG_list.append(p_bind_info[1])
    for p_bind_info in primer_2_bind_list_full[p2_id-1]:
        p_dG_list_full.append(p_bind_info[1])
    for p_bind_info in primer_pairs_bind_list[pp_id-1]:
        p_dG_list.append(p_bind_info[1])
    for p_bind_info in primer_pairs_bind_list_full[pp_id-1]:
        p_dG_list_full.append(p_bind_info[1])
    # 所有候选引物信息输出
    if report_out:
        REPORT.write("---------------------\n## PRIMER PAIR: %d\n" %pp_id)
        REPORT.write("Forward: 5' %s 3'\nReverse: 5' %s 3'\n" %(primer_info[0], primer_info[4]))
        REPORT.write("\nAmplicon Size: %d bases(%d - %d)\n" %(primer_info[8], primer_info[1], primer_info[5]))
        REPORT.write("\n### PRIMER DETAILS\n")
        REPORT.write("\nForward: %s (deltaG: %.2f)\nForward vs. Forward\n" %(primer_info[0], Tm(primer_info[0])[-1]))
        for p1_info in p1_bind_str_list_full:
            REPORT.write("ΔG: %.2f kcal/mol(%s)\n" % (p1_info[1], p1_info[2]))
            REPORT.write(Dimer_Align(p1_info[-1], p1_info[-1], p1_info[0], p1_info[2]))
            REPORT.write("\n")
        REPORT.write("\nReverse: %s (deltaG: %.2f)\nReverse vs. Reverse\n" %(primer_info[4], Tm(primer_info[4])[-1]))
        for p2_info in p2_bind_str_list_full:
            REPORT.write("ΔG: %.2f kcal/mol(%s)\n" % (p2_info[1], p2_info[2]))
            REPORT.write(Dimer_Align(p2_info[-1], p2_info[-1], p2_info[0], p2_info[2]))
            REPORT.write("\n")
        REPORT.write("\nForward vs. Reverse\n")
        for pp_info in pp_bind_str_list_full:
            REPORT.write("ΔG: %.2f kcal/mol(%s)\n" % (pp_info[1], pp_info[2]))
            REPORT.write(Dimer_Align(pp_info[-2], pp_info[-1], pp_info[0], pp_info[2]))
            REPORT.write("\n")
    # 正向引物检查
    if primer_info[0] in foward_primer_filter_by_dimer or primer_info[0] in foward_primer_filter_by_3_dimer:
        continue
    dimer_num = 0
    dimer_3_num = 0
    dG_0 = p1_bind_str_list_full[0][1]
    dG_0_3 = 999
    dimer_base_num = 0
    dimer_base_num_3 = 0
    dG_id = 0
    for bind_info in p1_bind_str_list_full:
        bind_str = bind_info[2]
        pl = len(bind_info[-1])
        k = bind_info[0]
        dG = bind_info[1]
        if dG_0 > dG:
            max_dG_id_p1 = dG_id
            dG_0 = dG
        dimer_count = bind_str.count('1')
        if dimer_base_num < dimer_count:
            dimer_base_num = dimer_count
            max_dimer_id_p1 = dG_id
        if dimer_num < dimer_count:
            dimer_num = dimer_count
        if k < pl - 1:
            dimer_num_3_1 = bind_str[-(max_3_dimer_total_num):].count('1')
            dimer_num_3_2 = bind_str[:max_3_dimer_total_num].count('1')
            if dimer_3_num < dimer_num_3_1:
                dimer_3_num = dimer_num_3_1
            if dimer_3_num < dimer_num_3_2:
                dimer_3_num = dimer_num_3_2
            if bind_str[0] == '1' or bind_str[-1] == '1':
                if dG_0_3 > dG:
                    dG_0_3 = dG
                    max_dG_id_p1_extend = dG_id
                if dimer_base_num_3 < dimer_count:
                    dimer_base_num_3 = dimer_count
                    max_dimer_id_p1_extend = dG_id
        dG_id += 1
    if exclude_max_dimer and dimer_num > max_dimer_basepair_num and primer_info[0] not in foward_primer_filter_by_dimer:
        max_dimer_filter_forward_num += 1
        foward_primer_filter_by_dimer.append(primer_info[0])
        continue
    if exclude_max_3_dimer and dimer_3_num > max_3_dimer_bp_num and primer_info[0] not in foward_primer_filter_by_3_dimer:
        max_3_dimer_filter_forward_num += 1
        foward_primer_filter_by_3_dimer.append(primer_info[0])
        continue
    # 反向引物检查
    if primer_info[4] in reverse_primer_filter_by_dimer or primer_info[4] in reverse_primer_filter_by_3_dimer:
        continue
    dimer_num = 0
    dimer_3_num = 0
    dG_0 = p2_bind_str_list_full[0][1]
    dG_0_3 = 999
    dimer_base_num = 0
    dimer_base_num_3 = 0
    dG_id = 0
    for bind_info in p2_bind_str_list_full:
        bind_str = bind_info[2]
        pl = len(bind_info[-1])
        k = bind_info[0]
        dG = bind_info[1]
        if dG_0 > dG:
            max_dG_id_p2 = dG_id
            dG_0 = dG
        dimer_count = bind_str.count('1')
        if dimer_base_num < dimer_count:
            dimer_base_num = dimer_count
            max_dimer_id_p2 = dG_id
        if dimer_num < dimer_count:
            dimer_num = dimer_count
        if k < pl - 1:
            dimer_num_3_1 = bind_str[-(max_3_dimer_total_num):].count('1')
            dimer_num_3_2 = bind_str[:max_3_dimer_total_num].count('1')
            if dimer_3_num < dimer_num_3_1:
                dimer_3_num = dimer_num_3_1
            if dimer_3_num < dimer_num_3_2:
                dimer_3_num = dimer_num_3_2
            if bind_str[0] == '1' or bind_str[-1] == '1':
                if dG_0_3 > dG:
                    dG_0_3 = dG
                    max_dG_id_p2_extend = dG_id
                if dimer_base_num_3 < dimer_count:
                    dimer_base_num_3 = dimer_count
                    max_dimer_id_p2_extend = dG_id
        dG_id += 1
    if exclude_max_dimer and dimer_num > max_dimer_basepair_num and primer_info[4] not in reverse_primer_filter_by_dimer:
        max_dimer_filter_reverse_num += 1
        reverse_primer_filter_by_dimer.append(primer_info[4])
        continue
    if exclude_max_3_dimer and dimer_3_num > max_3_dimer_bp_num and primer_info[4] not in reverse_primer_filter_by_3_dimer:
        max_3_dimer_filter_reverse_num += 1
        reverse_primer_filter_by_3_dimer.append(primer_info[4])
        continue
    # 引物对检查
    dimer_num = 0
    dimer_3_num = 0
    dG_0 = pp_bind_str_list_full[0][1]
    dG_0_3 = 999
    dimer_base_num = 0
    dimer_base_num_3 = 0
    dG_id = 0
    for bind_info in pp_bind_str_list_full:
        bind_str = bind_info[2]
        pl = max(len(bind_info[-1]), len(bind_info[-2]))
        k = bind_info[0]
        dG = bind_info[1]
        if dG_0 > dG:
            max_dG_id_pp = dG_id
            dG_0 = dG
        dimer_count = bind_str.count('1')
        if dimer_base_num < dimer_count:
            dimer_base_num = dimer_count
            max_dimer_id_pp = dG_id
        if dimer_num < dimer_count:
            dimer_num = dimer_count
        if k < pl - 1:
            dimer_num_3_1 = bind_str[-(max_3_dimer_total_num):].count('1')
            dimer_num_3_2 = bind_str[:max_3_dimer_total_num].count('1')
            if dimer_3_num < dimer_num_3_1:
                dimer_3_num = dimer_num_3_1
            if dimer_3_num < dimer_num_3_2:
                dimer_3_num = dimer_num_3_2
            if bind_str[0] == '1' or bind_str[-1] == '1':
                if dG_0_3 > dG:
                    dG_0_3 = dG
                    max_dG_id_pp_extend = dG_id
                if dimer_base_num_3 < dimer_count:
                    dimer_base_num_3 = dimer_count
                    max_dimer_id_pp_extend = dG_id
        dG_id += 1
    if exclude_max_dimer and dimer_num > max_dimer_basepair_num:
        max_dimer_filter_pp_num += 1
        continue
    if exclude_max_3_dimer and dimer_3_num > max_3_dimer_bp_num:
        max_3_dimer_filter_pp_num += 1
        continue
    primer_pair_num += 1
    if not args.simple_out and len(p_dG_list) > 0 and best_pp_dG_extand == min(p_dG_list):
        best_pp_str += ("## %d\n" %primer_pair_num)
        best_pp_str += ("Forward: 5' %s 3' (3'ΔG: %.2f kcal/mol)\nReverse: 5' %s 3' (3'ΔG: %.2f kcal/mol)\n" %(primer_info[0],Tm(primer_info[0][-5:])[3], primer_info[4], Tm(primer_info[4][-5:])[3]))
    '''if best_pp_dG_full == min(min_p1_dG_full, min_p2_dG_full, min_pp_dG_full, primer_info[10]):
        best_pp_str += ("## BEST PRIMER PAIR(full dimer concerned): %d\n" %primer_pair_num)
        best_pp_str += ("Forward: 5' %s 3'\nReverse: 5' %s 3'\n" %(primer_info[0], primer_info[4]))'''
    if not args.simple_out:
        out_str += ("---------------------\n## PRIMER PAIR: %d\n" %primer_pair_num)
        out_str += ("Forward: 5' %s 3'\nReverse: 5' %s 3'\n" %(primer_info[0], primer_info[4]))
        out_str += ("\nAmplicon Size: %d bases(%d - %d)\n" %(primer_info[8], primer_info[1], primer_info[5]))
        out_str += "\n### PRIMER DETAILS\n"
        out_str += ("\nForward primer: %s\n\n" % primer_info[0])
        Tm_1 = Tm(primer_info[0])
        out_str += ("Tm: %.2f ℃                Length: %d bases\nΔS: %.2f eu              ΔH: %.2f kcal/mol\nΔG(%d℃): %.2f kcal/mol   3'ΔG: %.2f kcal/mol\n\n" %(primer_info[3], primer_info[2], Tm_1[2], Tm_1[1], temperature, Tm_1[3], Tm(primer_info[0][-5:])[3]))
        out_str += ("\nReverse primer: %s\n\n" % primer_info[4])
        Tm_2 = Tm(primer_info[4])
        out_str += ("Tm: %.2f ℃                Length: %d bases\nΔS: %.2f eu              ΔH: %.2f kcal/mol\nΔG(%d℃): %.2f kcal/mol   3'ΔG: %.2f kcal/mol\n\n" %(primer_info[7], primer_info[6], Tm_2[2], Tm_2[1], temperature, Tm_2[3], Tm(primer_info[4][-5:])[3]))
        out_str += "### Most stable primer-dimers\n"
        out_str += ("Forward vs Forward: %.2f kcal/mol\n%s\n" % (p1_bind_str_list_full[max_dG_id_p1][1], Dimer_Align(p1_bind_str_list_full[max_dG_id_p1][-1], p1_bind_str_list_full[max_dG_id_p1][-1], p1_bind_str_list_full[max_dG_id_p1][0], p1_bind_str_list_full[max_dG_id_p1][2])))
        out_str += ("Forward vs Forward(3' extensible): %.2f kcal/mol\n%s\n" % (p1_bind_str_list_full[max_dG_id_p1_extend][1], Dimer_Align(p1_bind_str_list_full[max_dG_id_p1_extend][-1], p1_bind_str_list_full[max_dG_id_p1_extend][-1], p1_bind_str_list_full[max_dG_id_p1_extend][0], p1_bind_str_list_full[max_dG_id_p1_extend][2])))
        out_str += "### Most complementary-base primer-dimers\n"
        out_str += ("Forward vs Forward: %.2f kcal/mol\n%s\n" % (p1_bind_str_list_full[max_dimer_id_p1][1], Dimer_Align(p1_bind_str_list_full[max_dimer_id_p1][-1], p1_bind_str_list_full[max_dimer_id_p1][-1], p1_bind_str_list_full[max_dimer_id_p1][0], p1_bind_str_list_full[max_dimer_id_p1][2])))
        out_str += ("Forward vs Forward(3' extensible): %.2f kcal/mol\n%s\n" % (p1_bind_str_list_full[max_dimer_id_p1_extend][1], Dimer_Align(p1_bind_str_list_full[max_dimer_id_p1_extend][-1], p1_bind_str_list_full[max_dimer_id_p1_extend][-1], p1_bind_str_list_full[max_dimer_id_p1_extend][0], p1_bind_str_list_full[max_dimer_id_p1_extend][2])))
        out_str += "### Most stable primer-dimers\n"
        out_str += ("Reverse vs Reverse: %.2f kcal/mol\n%s\n" % (p2_bind_str_list_full[max_dG_id_p2][1], Dimer_Align(p2_bind_str_list_full[max_dG_id_p2][-1], p2_bind_str_list_full[max_dG_id_p2][-1], p2_bind_str_list_full[max_dG_id_p2][0], p2_bind_str_list_full[max_dG_id_p2][2])))
        out_str += ("Reverse vs Reverse(3' extensible): %.2f kcal/mol\n%s\n" % (p2_bind_str_list_full[max_dG_id_p2_extend][1], Dimer_Align(p2_bind_str_list_full[max_dG_id_p2_extend][-1], p2_bind_str_list_full[max_dG_id_p2_extend][-1], p2_bind_str_list_full[max_dG_id_p2_extend][0], p2_bind_str_list_full[max_dG_id_p2_extend][2])))
        out_str += "### Most complementary-base primer-dimers\n"
        out_str += ("Reverse vs Reverse: %.2f kcal/mol\n%s\n" % (p2_bind_str_list_full[max_dimer_id_p2][1], Dimer_Align(p2_bind_str_list_full[max_dimer_id_p2][-1], p2_bind_str_list_full[max_dimer_id_p2][-1], p2_bind_str_list_full[max_dimer_id_p2][0], p2_bind_str_list_full[max_dimer_id_p2][2])))
        out_str += ("Reverse vs Reverse(3' extensible): %.2f kcal/mol\n%s\n" % (p2_bind_str_list_full[max_dimer_id_p2_extend][1], Dimer_Align(p2_bind_str_list_full[max_dimer_id_p2_extend][-1], p2_bind_str_list_full[max_dimer_id_p2_extend][-1], p2_bind_str_list_full[max_dimer_id_p2_extend][0], p2_bind_str_list_full[max_dimer_id_p2_extend][2])))
        out_str += "### Most stable primer-dimers\n"
        out_str += ("Forward vs Reverse: %.2f kcal/mol\n%s\n" % (pp_bind_str_list_full[max_dG_id_pp][1], Dimer_Align(pp_bind_str_list_full[max_dG_id_pp][-2], pp_bind_str_list_full[max_dG_id_pp][-1], pp_bind_str_list_full[max_dG_id_pp][0], pp_bind_str_list_full[max_dG_id_pp][2])))
        out_str += ("Forward vs Reverse(3' extensible): %.2f kcal/mol\n%s\n" % (pp_bind_str_list_full[max_dG_id_pp_extend][1], Dimer_Align(pp_bind_str_list_full[max_dG_id_pp_extend][-2], pp_bind_str_list_full[max_dG_id_pp_extend][-1], pp_bind_str_list_full[max_dG_id_pp_extend][0], pp_bind_str_list_full[max_dG_id_pp_extend][2])))
        out_str += "### Most complementary-base primer-dimers\n"
        out_str += ("Forward vs Reverse: %.2f kcal/mol\n%s\n" % (pp_bind_str_list_full[max_dimer_id_pp][1], Dimer_Align(pp_bind_str_list_full[max_dimer_id_pp][-2], pp_bind_str_list_full[max_dimer_id_pp][-1], pp_bind_str_list_full[max_dimer_id_pp][0], pp_bind_str_list_full[max_dimer_id_pp][2])))
        out_str += ("Forward vs Reverse(3' extensible): %.2f kcal/mol\n%s\n" % (pp_bind_str_list_full[max_dimer_id_pp_extend][1], Dimer_Align(pp_bind_str_list_full[max_dG_id_pp_extend][-2], pp_bind_str_list_full[max_dG_id_pp_extend][-1], pp_bind_str_list_full[max_dG_id_pp_extend][0], pp_bind_str_list_full[max_dG_id_pp_extend][2])))
    else:
        ext_dG = min(p1_bind_str_list_full[max_dG_id_p1_extend][1], p2_bind_str_list_full[max_dG_id_p2_extend][1], pp_bind_str_list_full[max_dG_id_pp_extend][1])
        full_dG = min(p1_bind_str_list_full[max_dG_id_p1][1], p2_bind_str_list_full[max_dG_id_p2][1], pp_bind_str_list_full[max_dG_id_pp][1])
        OUT.write("%s\t%d\t%d\t%.2f\t%s\t%d\t%d\t%.2f\t%d\t%.2f\t%.2f\n" %(primer_info[0], primer_info[1], primer_info[2], primer_info[3], primer_info[4], primer_info[5], primer_info[6], primer_info[7], primer_info[8], ext_dG, full_dG))


print("过滤完毕，最终获得引物对: %d" %primer_pair_num)
print("写入文件中 ...")
if not args.simple_out:
    OUT.write(best_pp_str)
    OUT.write(out_str)
    OUT.close()
if report_out:
    REPORT.close()
print("成功写入文件: %s\n" %args.file_out)

# 引物过滤情况report
print("#########################")
print("## 引物过滤情况")
print("-------------------------")
print("所有可能的正向引物: %d" %all_possible_forward_num)
print("所有可能的反向引物: %d" %all_possible_reverse_num)
if exclude_gc and (GC_content_filter_forward_num or GC_content_filter_reverse_num):
    print("(GC含量范围: %d%% - %d%%)" %(min_gc, max_gc))
    print("正向引物中被GC含量过滤掉的数目: %d" %GC_content_filter_forward_num)
    print("反向引物中被GC含量过滤掉的数目: %d" %GC_content_filter_reverse_num)
if exclude_gc_clamp and (GC_clamp_filter_forward_num or GC_clamp_filter_reverse_num):
    print("正向引物中被GC帽子含量过滤掉的数目: %d" %GC_clamp_filter_forward_num)
    print("反向引物中被GC帽子含量过滤掉的数目: %d" %GC_clamp_filter_reverse_num)
if tm_filter_forward_num or tm_filter_reverse_num:
    print("(Tm值范围: %d ℃ - %d ℃)" %(min_tm, max_tm))
    print("正向引物中被Tm值过滤掉的数目: %d" %tm_filter_forward_num)
    print("反向引物中被Tm值过滤掉的数目: %d" %tm_filter_reverse_num)
if exclude_rr and (run_filter_forward_num or run_filter_reverse_num):
    print("(单碱基重复最大值: %d)" %run)
    print("正向引物中被单碱基重复过滤掉的数目: %d" %run_filter_forward_num)
    print("反向引物中被单碱基重复过滤掉的数目: %d" %run_filter_reverse_num)
if exclude_rr and (repeat_filter_forward_num or repeat_filter_reverse_num):
    print("(多碱基重复最大值: %d)" %repeat)
    print("正向引物中被多碱基重复过滤掉的数目: %d" %repeat_filter_forward_num)
    print("反向引物中被多碱基重复过滤掉的数目: %d" %repeat_filter_reverse_num)
print("\n#########################")
print("## 引物对过滤情况")
print("-------------------------")
print("候选引物对数目: %d" %all_pp_num)
if tm_diff_filter_pp_num:
    print("Tm最大差值: %d ℃" %max_tm_diff)
    print("候选引物对中被Tm差值过滤掉的数目: %d" %tm_diff_filter_pp_num)
if exclude_max_dimer:
    if max_dimer_filter_forward_num or max_dimer_filter_reverse_num or max_dimer_filter_pp_num:
        print("候选引物对正向引物被二聚体匹配碱基数过滤掉的数目: %d / %d" % (max_dimer_filter_forward_num, len(primer_1_bind_list)))
        print("候选引物对反向引物被二聚体匹配碱基数过滤掉的数目: %d / %d" % (max_dimer_filter_reverse_num, len(primer_2_bind_list)))
        print("候选引物对被二聚体匹配碱基数过滤掉的数目: %d" % max_dimer_filter_reverse_num)
if exclude_max_3_dimer:
    if max_3_dimer_filter_forward_num or max_3_dimer_filter_reverse_num or max_3_dimer_filter_pp_num:
        print("候选引物对正向引物被3'端二聚体匹配碱基数过滤掉的数目: %d / %d" % (max_3_dimer_filter_forward_num, len(primer_1_bind_list)))
        print("候选引物对反向引物被3'端二聚体匹配碱基数过滤掉的数目: %d / %d" % (max_3_dimer_filter_reverse_num, len(primer_2_bind_list)))
        print("候选引物对被3'端二聚体匹配碱基数过滤掉的数目: %d" % max_3_dimer_filter_pp_num)
print("----------------------------------------")
print("##最终获得引物对: %d" %primer_pair_num)


'''
if 0:
    print("Number P1-0:", len(primer_forward_list))
    print("Number P1:", len(primer_1_bind_list))
    print("Number P2-0:", len(primer_reverse_list))
    print("Number P2:", len(primer_2_bind_list))
    print("Number PP:", len(primer_pairs_bind_list))
    pp_id = 0
    for primer_info in primer_pairs_list:
        print(primer_info)
        pp_id += 1
        (p1_id, p2_id) = primer_info[-2:]
        print(p1_id, p2_id, pp_id)
        p1_bind_str_list = primer_1_bind_list[p1_id-1]
        p2_bind_str_list = primer_2_bind_list[p2_id-1]
        pp_bind_str_list = primer_pairs_bind_list[pp_id-1]
        print("P1 dimer info:", p1_bind_str_list[0][-1])
        for p1_info in p1_bind_str_list:
            #print(p1_info)
            print("K: %d Bind: %s DeltaG: %f" %(p1_info[0], p1_info[2], p1_info[1]))
            print(Dimer_Align(p1_info[-1], p1_info[-1], p1_info[0], p1_info[2]))
        print("P2 dimer info:", p2_bind_str_list[0][-1])
        for p2_info in p2_bind_str_list:
            #print(p2_info)
            print("K: %d Bind: %s DeltaG: %f" %(p2_info[0], p2_info[2], p2_info[1]))
            print(Dimer_Align(p2_info[-1], p2_info[-1], p2_info[0], p2_info[2]))
        print("PP dimer info:")
        for pp_info in pp_bind_str_list:
            #print(pp_info)
            print("K: %d Bind: %s DeltaG: %f" %(pp_info[0], pp_info[2], pp_info[1]))
            print(Dimer_Align(pp_info[-2], pp_info[-1], pp_info[0], pp_info[2]))
'''