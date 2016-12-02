#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
        FILE:SRAtools.ByExp.v1.0.py
       USAGE: $ SRAtools.ByExp.v1.0 -h
 DESCRIPTION: 在网站NCBI-SRA(https://www.ncbi.nlm.nih.gov/sra/) 中查询指定
              accession(库或实验编号)或accession列表文件对应的sra run信息，
              包括列表及其ftp链接等，并提供2中下载方案。
     OPTIONS: -accession
REQUIREMENTS: accession id, i.e. SRX100741
        BUGS: bugs
      AUTHOR: guochangjiang(polaris)
     CONTACT: guochangjiang1989@gmail.com
ORGANIZATION: Nanjing University, China
     VERSION: 1.0
     CREATED: 2016/12/1 16:36:05
      UPDATE: 2016/12/1 16:36:05

 CHANGE LOGS:
     Version 1.0 2016/12/1 16:36:05    初始版本
'''

import argparse
import re
import os
import requests
import urllib

__version__ = '1.0'

# 命令行参数
parser = argparse.ArgumentParser()
parser.add_argument(
                    "-acc",
                    "-accession",
                    "--accession_id",
                    metavar="accession_id",
                    dest="accession_id",
                    default="",
                    #required=True,
                    type=str,
                    help="accession id list, i.e. SRX100741,SRX100741")
parser.add_argument(
                    "-acc_file",
                    "-accession_file",
                    "--accession_id_list_file",
                    metavar="accession_id_list_file",
                    dest="accession_id_list_file",
                    #required=True,
                    default="",
                    type=str,
                    help="text file of accession id list(single id each line)")
parser.add_argument(
                    "-v", "--version",
                    action='version',
                    help="The version of this program.",
                    version="Version: " + __version__)
args = parser.parse_args()

# accession list
accession_id_list = []
if args.accession_id:
    accession_id_list = args.accession_id.split(",")
if args.accession_id_list_file:
    with open(args.accession_id_list_file) as LIST:
        for line in LIST:
            line = line.strip()
            if line == "":
                continue
            if line not in accession_id_list:
                accession_id_list.append(line)
if accession_id_list == []:
    print("No accession id found!")
    os._exit(0)

#sra info from NCBI sra
for acc in accession_id_list:
    url_site = "https://www.ncbi.nlm.nih.gov/sra/" + acc
    r = requests.get(url_site)
    if "Page not found - SRA - NCBI" in r.text or "The requested page does not exist" in r.text:
        print("accession id %s is not found! Please check it.")
        os._exit(0)
    lines = r.text.splitlines()
    title_info = ''
    main_info = ''
    accession_title = ''
    sequencing_platform = ''
    submitted_by = ''
    study = ''
    sample = ''
    organism = ''
    Library_info = {
        'Name': '',
        'Instrument': '',
        'Strategy': '',
        'Source': '',
        'Selection': '',
        'Layout': '',
    }
    runs_results = ''
    run_num = 0
    run_id_list = []
    run_info_dict = {}
    for line in lines:
        line = line.strip()
        #print(line)
        line = line.encode("GBK", "ignore").decode('utf-8')
        #print(line)
        if "<title>" in line:
            title_info = line
            title_info = title_info[7:-8]
        if "<div><p class=\"details expand e-hidden\">" in line:
            main_info = line
            #print(main_info)
            m = re.search(r"</a>:\s*(.+?)</b>", main_info)
            accession_title = m.group(1)
            m = re.search(r"</b><br />(.+?)</p>", main_info)
            sequencing_platform = m.group(1)
            m = re.search(r"Submitted by: <span>(.+?)</span>", main_info)
            submitted_by = m.group(1)
            m = re.search(r"Study: <span>(.+?)<", main_info)
            study = m.group(1)
            m = re.search(r"Sample: <span>(.+?)<", main_info)
            sample = m.group(1)
            m = re.search(r"Organism: <span><a href=.+?>(.+?)<", main_info)
            organism = m.group(1)
            m = re.search(r"Name: <span>(.+?)<", main_info)
            Library_info['Name'] = m.group(1)
            m = re.search(r"Instrument: <span>(.+?)<", main_info)
            Library_info['Instrument'] = m.group(1)
            m = re.search(r"Strategy: <span>(.+?)<", main_info)
            Library_info['Strategy'] = m.group(1)
            m = re.search(r"Source: <span>(.+?)<", main_info)
            Library_info['Source'] = m.group(1)
            m = re.search(r"Selection: <span>(.+?)<", main_info)
            Library_info['Selection'] = m.group(1)
            m = re.search(r"Layout: <span>(.+?)<", main_info)
            Library_info['Layout'] = m.group(1)
            m = re.search(r"Runs: <span>(.+?)<", main_info)
            runs_results = m.group(1)
            m = re.search(r"All runs for this experiment\">(.+?)<", main_info)
            runs_results = runs_results + "size:" + m.group(1)
            m = re.search(r"<span>(\d+) run", main_info)
            run_num = int(m.group(1))
            fa = re.findall(r'run=(\w+)">', main_info)
            run_id_list = fa
            for run in run_id_list:
                regex = re.compile(r'run=%s">%s</a></td><td align="right">(.+?)</td><td align="right">(.+?)</td><td align="right">(.+?)</td><td>(.+?)</td>' %(run, run))
                m = regex.search(main_info)
                run_info_dict[run] = []
                run_info_dict[run]= [m.group(1),m.group(2),m.group(3),m.group(4)]
    
    ftp_link_pre = "ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByExp/sra/" + args.accession_id[0:3].upper() + "/" + args.accession_id[0:6].upper() + "/" + args.accession_id.upper() + "/"
    
    print("title info:", title_info)
    #print("main info:", main_info)
    print("accession title:", accession_title)
    print("sequencing platform:", sequencing_platform)
    print("submitted by:", submitted_by)
    print("study:", study)
    print("sample:", sample)
    print("organism:", organism)
    print(Library_info['Name'])
    print(Library_info['Instrument'])
    print(Library_info['Strategy'])
    print(Library_info['Source'])
    print(Library_info['Selection'])
    print(Library_info['Layout'])
    print("runs_results:", runs_results)
    print("run num: %d" %run_num)
    for run_id in run_id_list:
        print("run: %s" %run_id)
        print(ftp_link_pre + run_id.upper() + "/" + run_id.upper() + ".sra")
        urllib.request.urlretrieve(ftp_link_pre + run_id.upper() + "/" + run_id.upper() + ".sra", run_id.upper() + ".sra")