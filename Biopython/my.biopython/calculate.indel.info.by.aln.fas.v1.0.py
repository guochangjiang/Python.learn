#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: calculate.indel.info.by.aln.fas.v1.0.py
       USAGE: $ python calculate.indel.info.by.aln.fas.v1.0.py -h
 DESCRIPTION: 根据提供的比对过的fasta文件和指定的window length与step size
              信息，计算indel位点的数目信息用于图形绘制
     OPTIONS: -i [xx.fasta] -window [N] -step [n] -o [output]
REQUIREMENTS: fasta file(alignment)
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/5/6 16:20:30
      UPDATE: 2016/5/6 16:20:30

 CHANGE LOGS:
     Version 1.0 2016/5/6 16:20:30    初始版本: indel计数方式有2种：单位点计数与连续位点合并计数
                                                最终的indel_num为占少数的类型(insertion or deletion)的数目
'''

#子例程

def Count_InDel_by_point(seqs):
    seq_length = len(seqs[0])
    indel_number = 0
    insertion_number = 0
    deletion_number = 0
    for i in range(seq_length):
        for seq in seqs:
            seq_at_same_index += seq[i]
        deletion_count = seq_at_same_index.count('-')
        N_count = seq_at_same_index.count('N')
        insertion_count = len(seq_at_same_index) - deletion_count - N_count
        insertion_number += insertion_count
        deletion_number += deletion_count
        if insertion_count > deletion_count:
            indel_number += deletion_count
        else:
            indel_number += insertion_count
    return(indel_number, insertion_number, deletion_number)

def Count_InDel_by_merge(seqs):
    pass
    
import argparse

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
                    help="fasta file to input")
parser.add_argument(
                    "-o",
                    "-out",
                    "--output",
                    metavar="output_file",
                    dest="file_out",
                    default="",
                    type=str,
                    help="file to output, [default: input.indel.info.out]")
parser.add_argument(
                    "-w",
                    "-window",
                    "--window_length",
                    metavar="length of window",
                    dest="window_length",
                    default= 100,
                    type=int,
                    help="window length, [default: 100]")
parser.add_argument(
                    "-s",
                    "-step",
                    "--step_size",
                    metavar="size of step",
                    dest="step_size",
                    default= 25,
                    type=int,
                    help="window length, [default: 25]")
parser.add_argument(
                    "-m",
                    "-mode",
                    "--count_mode",
                    metavar="mode of count indel",
                    dest="count_mode",
                    default= 'both',
                    type=str,
                    help="mode of count indel, e.g. point, merge, and both [default: both]")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

fasta_file = args.fasta_in
if args.file_out == '':
    out_file = fasta_file
    out_file = re.sub('\w+$','indel.info.out')
else:
    out_file = args.file_out

count_mode = args.count_mode
window_length = args.window_length
step_size = args.step_size

#输出文件头行信息
head_line = "ID\tcount_mode\twindow_length\tstep_size\tseq_number\twindow_id\twindow_start\twindow_end\tindel_number\tinsertion_num\tdeletion_number\n"
OUT = open(out_file, 'w')
OUT.write(head_line)
sequence_dict = {}
seqname_list = []
name = ''
with open(fasta_file) as FAS:
    for line in FAS:
        line = line.strip()
        if line == '':
            continue
        if line[0] == ">":
            name = line[1:]
            if name not in seqname_list:
                seqname_list.append(name)
                sequence_dict[name] = ''
        else:
            sequence_dict[name] += line

#按window进行统计
seq_number = len(seqname_list)
count = 0
while 1:
    window_start = count * step_size + 1
    window_end = count * step_size + window_length
    window_id = count + 1
    count += 1
    if window_end >= len(sequence_dict[seqname_list[0]]):
        window_end = len(sequence_dict[seqname_list[0]])
    window_seq = []
    for seqname in seqname_list:
        window_seq.append(sequence_dict[seqname][window_start-1:window_end])
    if args.count_mode in ['point', 'both']:
        (indel_num, insertion_num, deletion_num) = Count_InDel_by_point(window_seq)
        OUT.write('%s\tpoint\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' %(fasta_file, window_length, step_size, seq_number, window_id, window_start, window_end, indel_num, insertion_num, deletion_num))
    if args.count_mode in ['merge', 'both']:
        pass
        #(indel_num, insertion_num, deletion_num) = Count_InDel_by_merge(window_seq)
        #OUT.write('%s\tmerge\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\n' %(fasta_file, window_length, step_size, seq_number, window_id, window_start, window_end, indel_num, insertion_num, deletion_num))
    if window_end == len(sequence_dict[seqname_list[0]]):
        break
    OUT.close()