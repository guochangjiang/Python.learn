#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE: CalDimerDeltaG.v1.1.py
       USAGE: $ python CalDimerDeltaG.v1.1.py -h
 DESCRIPTION: Calculate deltaG of DNA Oligo dimer by nearest-neighbor thermodynamics assembled by John SantaLucia
     OPTIONS: options
REQUIREMENTS: requirements
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.1
     CREATED: 2016/6/21 18:48:09
      UPDATE: 2016/6/21 18:48:09

 CHANGE LOGS:
     Version 1.0 2016/6/21 18:48:09    初始版本: 按照邻近热力学(nearest-neighbor thermodynamics)计算指定DNA oligo的dimer的ΔG值
     Version 1.1 2016/6/23 10:33:10    新增: 按照oligo 7中对不连续碱基配对二聚体进行重新组合后取最小ΔG值
'''

import argparse
import math

__version__ = '1.1'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-seq",
                    "--sequence_forward",
                    metavar="forward oligo sequence",
                    dest="sequence_forward",
                    required=True,
                    type=str,
                    help="forward DNA oligo sequence(5' -> 3')")
parser.add_argument(
                    "-cseq",
                    "--sequence_complement",
                    metavar="complement oligo sequence",
                    dest="sequence_complement",
                    default=None,
                    type=str,
                    help="reverse DNA oligo sequence(3' -> 5')[default: the complement sequence of forward DNA oligo]")
parser.add_argument(
                    "-shift",
                    "--forward_sequnce_shift_distance",
                    metavar="forward sequnce shift distance",
                    dest="shift",
                    default=0,
                    type=int,
                    help="bases of forward sequence moves to right to form dimer with complement sequence[default:0]")
parser.add_argument(
                    '-no_oligo7',
                    "--not_use_oligo7",
                    action='store_true',
                    default=False,
                    dest='no_oligo7',
                    help="not use parameters in oligo7")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()


# global variables
# PCR conditions(Oligo 7)
oligo_conc_oligo7 = 200.0                           # 引物浓度(nM)
Mg_conc_oligo7 = 0.7                                # 镁离子浓度(mM), generally 1.5mM
monovalent_cation_conc_oligo7 = 50.0                # 一价阳离子 Mon = Na + K + Tris/2(mM)
Na_conc_oligo7 = 50.0                               # 钠离子浓度(mM)
K_conc_oligo7 = 0                                   # 钾离子浓度(mM)
Tris_conc_oligo7 = 0                                # Tris离子浓度(mM)
Na_Eq = 155.8                                       # Na equivalent(mM) = monovalent_cation_conc + 120 * sqrt(Mg_conc - dNTP_conc)(Oligo 7: Na_eq=monovalent_cation_conc+126.4911*sqrt(Mg_conc))
dNTP_conc_oligo7 = 0.2                              # dNTP浓度(mM)
temp_deltaG_oligo7 = 25.0                           # 计算ΔG时的温度(Oligo 7 default: 25°C)

# PCR conditions(in general)
oligo_conc = 200.0                                  # 引物浓度(nM)
Mg_conc = 1.5                                       # 镁离子浓度(mM), generally 1.5mM
monovalent_cation_conc = 50.0                       # 一价阳离子 Mon = Na + K + Tris/2(mM)
Na_conc = 50.0                                      # 钠离子浓度(mM)
K_conc = 0                                          # 钾离子浓度(mM)
Tris_conc = 0                                       # Tris离子浓度(mM)
dNTP_conc = 0.2                                     # dNTP浓度(mM)
temp_deltaG = 25.0                                  # 计算ΔG时的温度(Oligo 7 default: 25°C)

# base pair
BasePairs = ("AT", "TA", "GC", "CG")
# Thermodynamic lookup tables (dictionaries):
# Enthalpy (dH) and entropy (dS) values for nearest neighbors and initiation
# process. Calculation of duplex initiation is quite different in several
# papers; to allow for a general calculation, all different initiation
# parameters are included in all tables and non-applicable parameters are set
# to zero.
# The key is either an initiation type (e.g., 'init_A/T') or a nearest neighbor
# duplex sequence (e.g., GT/CA, to read 5'GT3'-3'CA5'). The values are tuples
# of dH (kcal/mol), dS (cal/mol K).
# ΔH(kcal/mol), ΔS(cal/mol K) (NN parameters in 1M NaCl pH7 at 37°C)
# DNA/DNA
# Allawi and SantaLucia (1997), Biochemistry 36: 10581-10594

Oligo_dH_dS = {
    'init': (0, 0), 'init_A/T': (2.3, 4.1), 'init_G/C': (0.1, -2.8),
    'init_oneG/C': (0, 0), 'init_allA/T': (0, 0), 'init_5T/A': (0, 0),
    'sym': (0, -1.4),
    'AA/TT': (-7.9, -22.2), 'AT/TA': (-7.2, -20.4), 'TA/AT': (-7.2, -21.3),
    'CA/GT': (-8.5, -22.7), 'GT/CA': (-8.4, -22.4), 'CT/GA': (-7.8, -21.0),
    'GA/CT': (-8.2, -22.2), 'CG/GC': (-10.6, -27.2), 'GC/CG': (-9.8, -24.4),
    'GG/CC': (-8.0, -19.9),
    # Internal mismatch and inosine table (DNA)
    # Allawi & SantaLucia (1997), Biochemistry 36: 10581-10594
    # Allawi & SantaLucia (1998), Biochemistry 37: 9435-9444
    # Allawi & SantaLucia (1998), Biochemistry 37: 2170-2179
    # Allawi & SantaLucia (1998), Nucl Acids Res 26: 2694-2701
    # Peyret et al. (1999), Biochemistry 38: 3468-3477
    # Watkins & SantaLucia (2005), Nucl Acids Res 33: 6258-6267
    'AG/TT': (1.0, 0.9), 'AT/TG': (-2.5, -8.3), 'CG/GT': (-4.1, -11.7),
    'CT/GG': (-2.8, -8.0), 'GG/CT': (3.3, 10.4), 'GG/TT': (5.8, 16.3),
    'GT/CG': (-4.4, -12.3), 'GT/TG': (4.1, 9.5), 'TG/AT': (-0.1, -1.7),
    'TG/GT': (-1.4, -6.2), 'TT/AG': (-1.3, -5.3), 'AA/TG': (-0.6, -2.3),
    'AG/TA': (-0.7, -2.3), 'CA/GG': (-0.7, -2.3), 'CG/GA': (-4.0, -13.2),
    'GA/CG': (-0.6, -1.0), 'GG/CA': (0.5, 3.2), 'TA/AG': (0.7, 0.7),
    'TG/AA': (3.0, 7.4),
    'AC/TT': (0.7, 0.2), 'AT/TC': (-1.2, -6.2), 'CC/GT': (-0.8, -4.5),
    'CT/GC': (-1.5, -6.1), 'GC/CT': (2.3, 5.4), 'GT/CC': (5.2, 13.5),
    'TC/AT': (1.2, 0.7), 'TT/AC': (1.0, 0.7),
    'AA/TC': (2.3, 4.6), 'AC/TA': (5.3, 14.6), 'CA/GC': (1.9, 3.7),
    'CC/GA': (0.6, -0.6), 'GA/CC': (5.2, 14.2), 'GC/CA': (-0.7, -3.8),
    'TA/AC': (3.4, 8.0), 'TC/AA': (7.6, 20.2),
    'AA/TA': (1.2, 1.7), 'CA/GA': (-0.9, -4.2), 'GA/CA': (-2.9, -9.8),
    'TA/AA': (4.7, 12.9), 'AC/TC': (0.0, -4.4), 'CC/GC': (-1.5, -7.2),
    'GC/CC': (3.6, 8.9), 'TC/AC': (6.1, 16.4), 'AG/TG': (-3.1, -9.5),
    'CG/GG': (-4.9, -15.3), 'GG/CG': (-6.0, -15.8), 'TG/AG': (1.6, 3.6),
    'AT/TT': (-2.7, -10.8), 'CT/GT': (-5.0, -15.8), 'GT/CT': (-2.2, -8.4),
    'TT/AT': (0.2, -1.5),
    'AI/TC': (-8.9, -25.5), 'TI/AC': (-5.9, -17.4), 'AC/TI': (-8.8, -25.4),
    'TC/AI': (-4.9, -13.9), 'CI/GC': (-5.4, -13.7), 'GI/CC': (-6.8, -19.1),
    'CC/GI': (-8.3, -23.8), 'GC/CI': (-5.0, -12.6),
    'AI/TA': (-8.3, -25.0), 'TI/AA': (-3.4, -11.2), 'AA/TI': (-0.7, -2.6),
    'TA/AI': (-1.3, -4.6), 'CI/GA': (2.6, 8.9), 'GI/CA': (-7.8, -21.1),
    'CA/GI': (-7.0, -20.0), 'GA/CI': (-7.6, -20.2),
    'AI/TT': (0.49, -0.7), 'TI/AT': (-6.5, -22.0), 'AT/TI': (-5.6, -18.7),
    'TT/AI': (-0.8, -4.3), 'CI/GT': (-1.0, -2.4), 'GI/CT': (-3.5, -10.6),
    'CT/GI': (0.1, -1.0), 'GT/CI': (-4.3, -12.1),
    'AI/TG': (-4.9, -15.8), 'TI/AG': (-1.9, -8.5), 'AG/TI': (0.1, -1.8),
    'TG/AI': (1.0, 1.0), 'CI/GG': (7.1, 21.3), 'GI/CG': (-1.1, -3.2),
    'CG/GI': (5.8, 16.9), 'GG/CI': (-7.6, -22.0),
    'AI/TI': (-3.3, -11.9), 'TI/AI': (0.1, -2.3), 'CI/GI': (1.3, 3.0),
    'GI/CI': (-0.5, -1.3),
    # Dangling ends table (DNA)
    # Bommarito et al. (2000), Nucl Acids Res 28: 1929-1934
    'AA/.T': (0.2, 2.3), 'AC/.G': (-6.3, -17.1), 'AG/.C': (-3.7, -10.0),
    'AT/.A': (-2.9, -7.6), 'CA/.T': (0.6, 3.3), 'CC/.G': (-4.4, -12.6),
    'CG/.C': (-4.0, -11.9), 'CT/.A': (-4.1, -13.0), 'GA/.T': (-1.1, -1.6),
    'GC/.G': (-5.1, -14.0), 'GG/.C': (-3.9, -10.9), 'GT/.A': (-4.2, -15.0),
    'TA/.T': (-6.9, -20.0), 'TC/.G': (-4.0, -10.9), 'TG/.C': (-4.9, -13.8),
    'TT/.A': (-0.2, -0.5),
    '.A/AT': (-0.7, -0.8), '.C/AG': (-2.1, -3.9), '.G/AC': (-5.9, -16.5),
    '.T/AA': (-0.5, -1.1), '.A/CT': (4.4, 14.9), '.C/CG': (-0.2, -0.1),
    '.G/CC': (-2.6, -7.4), '.T/CA': (4.7, 14.2), '.A/GT': (-1.6, -3.6),
    '.C/GG': (-3.9, -11.2), '.G/GC': (-3.2, -10.4), '.T/GA': (-4.1, -13.1),
    '.A/TT': (2.9, 10.4), '.C/TG': (-4.4, -13.1), '.G/TC': (-5.2, -15.0),
    '.T/TA': (-3.8, -12.6)
    }
# Terminal mismatch table (DNA)
# SantaLucia & Peyret (2001) Patent Application WO 01/94611
Oligo_dH_dS_TMM = {
    'AA/TA': (-3.1, -7.8), 'TA/AA': (-2.5, -6.3), 'CA/GA': (-4.3, -10.7),
    'GA/CA': (-8.0, -22.5),
    'AC/TC': (-0.1, 0.5), 'TC/AC': (-0.7, -1.3), 'CC/GC': (-2.1, -5.1),
    'GC/CC': (-3.9, -10.6),
    'AG/TG': (-1.1, -2.1), 'TG/AG': (-1.1, -2.7), 'CG/GG': (-3.8, -9.5),
    'GG/CG': (-0.7, -19.2),
    'AT/TT': (-2.4, -6.5), 'TT/AT': (-3.2, -8.9), 'CT/GT': (-6.1, -16.9),
    'GT/CT': (-7.4, -21.2),
    'AA/TC': (-1.6, -4.0), 'AC/TA': (-1.8, -3.8), 'CA/GC': (-2.6, -5.9),
    'CC/GA': (-2.7, -6.0), 'GA/CC': (-5.0, -13.8), 'GC/CA': (-3.2, -7.1),
    'TA/AC': (-2.3, -5.9), 'TC/AA': (-2.7, -7.0),
    'AC/TT': (-0.9, -1.7), 'AT/TC': (-2.3, -6.3), 'CC/GT': (-3.2, -8.0),
    'CT/GC': (-3.9, -10.6), 'GC/CT': (-4.9, -13.5), 'GT/CC': (-3.0, -7.8),
    'TC/AT': (-2.5, -6.3), 'TT/AC': (-0.7, -1.2),
    'AA/TG': (-1.9, -4.4), 'AG/TA': (-2.5, -5.9), 'CA/GG': (-3.9, -9.6),
    'CG/GA': (-6.0, -15.5), 'GA/CG': (-4.3, -11.1), ' GG/CA': (-4.6, -11.4),
    'TA/AG': (-2.0, -4.7), 'TG/AA': (-2.4, -5.8),
    'AG/TT': (-3.2, -8.7), 'AT/TG': (-3.5, -9.4), 'CG/GT': (-3.8, -9.0),
    'CT/GG': (-6.6, -18.7), 'GG/CT': (-5.7, -15.9), 'GT/CG': (-5.9, -16.1),
    'TG/AT': (-3.9, -10.5), 'TT/AG': (-3.6, -9.8),
}
salt_correction = 0
Na_eq = 0
entropy_adjust = 0
if args.no_oligo7:
    if Mg_conc > dNTP_conc:
        salt_correction = math.sqrt(Mg_conc - dNTP_conc)
    Na_eq=(monovalent_cation_conc + 120 * salt_correction)/1000 # mM -> M
    entropy_adjust = (0.368 * math.log(Na_eq))
else:
    salt_correction = math.sqrt(Mg_conc_oligo7)
    Na_eq=(monovalent_cation_conc_oligo7 + 126.4911 * salt_correction)/1000 # mM -> M
    entropy_adjust = (0.368 * math.log(Na_eq))
#Oligo_dG = {}
#for key in Oligo_dH_dS:
#    Oligo_dG[key] = Oligo_dH_dS[key][0] - (273.15 + 37) * (Oligo_dH_dS[key][1]) / 1000 # dG = dH - TdS (perlprimer:dG = dH - T(dS + entropy_adjust))
#    #print(key, Oligo_dG[key])

# subroutines
# 互补序列
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
                    'U':'A', 'u':'a',
                    }
    letters = list(DNA)
    letters = [basecomplement[base] for base in letters]
    return ''.join(letters)
# dimer重组
def DimerRecombination(s1, s2):
    dimer_list = []
    dimer_matirx = ''
    for i in range(len(s1)-1):
        if s1[i]+s2[i] in BasePairs:
            dimer_matirx += '1'                 # 可配对
        elif s1[i] == '.' or s2[i] == '.':
            dimer_matirx += '2'                 # 其一为空
        else:
            dimer_matirx += '0'                 # 不可配对
    if dimer_matirx[1:len(dimer_matirx)-1].count('1') == len(dimer_matirx) - 2:
        dimer_list.append([s1, s2])
        return dimer_list
    else:
        

# main
shift = args.shift
sequence_f = args.sequence_forward
sequence_c = args.sequence_complement
if sequence_c == None:
    sequence_c = Complement(sequence_f)
sequence_f = sequence_f.upper()
sequence_c = sequence_c.upper()
delta_h = 0
delta_s = 0
d_h = 0  # Names for indexes
d_s = 1  # 0 and 1
# simplify dimer sequence
# 长度归一化
if shift or len(sequence_f) != len(sequence_c):
    if shift > 0:
        sequence_f = '.' * shift + sequence_f
    if shift < 0:
        sequence_c = '.' * abs(shift) + sequence_c
    if len(sequence_c) > len(sequence_f):
        sequence_f += '.' * (len(sequence_c) - len(sequence_f))
    if len(sequence_c) < len(sequence_f):
        sequence_c += '.' * (len(sequence_f) - len(sequence_c))
# 末端修剪
while (sequence_f[0] + sequence_c[0]) not in BasePairs and (sequence_f[1] + sequence_c[1]) not in BasePairs:
    sequence_f = sequence_f[1:]
    sequence_c = sequence_c[1:]
    print(sequence_f)
    print(sequence_c)
while (sequence_f[-2] + sequence_c[-2]) not in BasePairs and (sequence_f[-1] + sequence_c[-1]) not in BasePairs:
    sequence_f = sequence_f[:-1]
    sequence_c = sequence_c[:-1]
sequence_f_c = DimerRecombination(sequence_f, sequence_c)

# Dangling ends?
if shift or len(sequence_f) != len(sequence_c):
    if shift > 0:
        sequence_f = '.' * shift + sequence_f
    if shift < 0:
        sequence_c = '.' * abs(shift) + sequence_c
    if len(sequence_c) > len(sequence_f):
        sequence_f += '.' * (len(sequence_c) - len(sequence_f))
    if len(sequence_c) < len(sequence_f):
        sequence_c += '.' * (len(sequence_f) - len(sequence_c))
    # Remove 'over-dangling' ends
    while sequence_f[:2] == '..' or sequence_c[:2] == '..':
        sequence_f = sequence_f[1:]
        sequence_c = sequence_c[1:]
    while sequence_f[-2:] == '..' or sequence_c[-2:] == '..':
        sequence_f = sequence_f[:-1]
        sequence_c = sequence_c[:-1]
    # Now for the dangling ends
    if sequence_f[0] == '.' or sequence_c[0] == '.':
        left_de = sequence_f[:2] + '/' + sequence_c[:2]
        if left_de in Oligo_dH_dS:
            delta_h += Oligo_dH_dS[left_de][d_h]
            delta_s += Oligo_dH_dS[left_de][d_s]
            sequence_f = sequence_f[1:]
            sequence_c = sequence_c[1:]
        elif left_de[::-1] in Oligo_dH_dS:
            delta_h += Oligo_dH_dS[left_de[::-1]][d_h]
            delta_s += Oligo_dH_dS[left_de[::-1]][d_s]
            sequence_f = sequence_f[1:]
            sequence_c = sequence_c[1:]
    if sequence_f[-1] == '.' or sequence_c[-1] == '.':
        right_de = sequence_f[-2:] + '/' + sequence_c[-2:]
        if right_de in Oligo_dH_dS:
            delta_h += Oligo_dH_dS[right_de][d_h]
            delta_s += Oligo_dH_dS[right_de][d_s]
            sequence_f = sequence_f[:-1]
            sequence_c = sequence_c[:-1]
        elif right_de[::-1] in Oligo_dH_dS:
            delta_h += Oligo_dH_dS[right_de[::-1]][d_h]
            delta_s += Oligo_dH_dS[right_de[::-1]][d_s]
            sequence_f = sequence_f[:-1]
            sequence_c = sequence_c[:-1]
print(sequence_f)
print(sequence_c)
# Now for terminal mismatches
while (sequence_f[0] + sequence_c[0]) not in BasePairs and (sequence_f[1] + sequence_c[1]) not in BasePairs:
    sequence_f = sequence_f[1:]
    sequence_c = sequence_c[1:]
    print(sequence_f)
    print(sequence_c)
while (sequence_f[-2] + sequence_c[-2]) not in BasePairs and (sequence_f[-1] + sequence_c[-1]) not in BasePairs:
    sequence_f = sequence_f[:-1]
    sequence_c = sequence_c[:-1]
left_tmm = sequence_c[:2][::-1] + '/' + sequence_f[:2][::-1]
if left_tmm in Oligo_dH_dS_TMM:
    if args.no_oligo7:
        delta_h += Oligo_dH_dS_TMM[left_tmm][d_h]
        delta_s += Oligo_dH_dS_TMM[left_tmm][d_s]
    sequence_f = sequence_f[1:]
    sequence_c = sequence_c[1:]
right_tmm = sequence_f[-2:] + '/' + sequence_c[-2:]
if right_tmm in Oligo_dH_dS_TMM:
    if args.no_oligo7:
        delta_h += Oligo_dH_dS_TMM[right_tmm][d_h]
        delta_s += Oligo_dH_dS_TMM[right_tmm][d_s]
    sequence_f = sequence_f[:-1]
    sequence_c = sequence_c[:-1]
# Now everything 'unusual' at the ends is handled and removed and we can
# look at the initiation.
terminal_bases = sequence_f[0] + sequence_f[-1]
AT_count = terminal_bases.count('A') + terminal_bases.count('T')
GC_count = terminal_bases.count('G') + terminal_bases.count('C')
delta_h += Oligo_dH_dS['init_A/T'][d_h] * AT_count
delta_s += Oligo_dH_dS['init_A/T'][d_s] * AT_count
delta_h += Oligo_dH_dS['init_G/C'][d_h] * GC_count
delta_s += Oligo_dH_dS['init_G/C'][d_s] * GC_count
# Finally, the 'zipping'
for basenumber in range(len(sequence_f) - 1):
    neighbors = sequence_f[basenumber:basenumber + 2] + '/' + sequence_c[basenumber:basenumber + 2]
    if neighbors in Oligo_dH_dS:
        delta_h += Oligo_dH_dS[neighbors][d_h]
        delta_s += Oligo_dH_dS[neighbors][d_s]
    elif neighbors[::-1] in Oligo_dH_dS:
        delta_h += Oligo_dH_dS[neighbors[::-1]][d_h]
        delta_s += Oligo_dH_dS[neighbors[::-1]][d_s]
    else:
        pass
k = oligo_conc * 1e-9
R = 1.987  # universal gas constant in Cal/degrees C*Mol
delta_s_corr = delta_s + entropy_adjust
melting_temp = (1000 * delta_h) / (delta_s_corr + (R * (math.log(k/4)))) - 273.15
delta_g_25_corr = delta_h - ((273.15 + 25)*(delta_s_corr/1000))
delta_g_25 = delta_h - ((273.15 + 25)*(delta_s/1000))  # oligo 7
print("ΔH:",delta_h)    # oligo 7
print("ΔS:",delta_s)    # oligo 7
print("ΔS corr:",delta_s_corr)
print("ΔG-25-corr:", delta_g_25_corr)
print("ΔG-25:", delta_g_25) # oligo 7
print("Tm:", melting_temp)