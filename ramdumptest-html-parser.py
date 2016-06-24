import os
import re
import sys
import math
import signal
import socket
import timeit
import platform
import threading
import binascii
import codecs
import re
import ssl
import requests
import fnmatch
import subprocess


from lxml import etree
from lxml import html


# with open('ITS_test.html', 'r', encoding = 'utf-8') as input_file:
    # data=input_file.read()
    # contentTree = html.fromstring(data)
    # project = []
    # project.append(contentTree.xpath('//*[@id="j_id182"]/table/tbody/tr[1]/td[1]/span/text()'))
    # project.append(contentTree.xpath('//*[@id="nos"]/text()'))
    # print(project)

# contentTree = etree.HTML(requests.get(url='http://econpy.pythonanywhere.com/ex/001.html').content.decode('utf-8'))
# buyers = contentTree.xpath('//div[@title="buyer-name"]/text()')
# prices = contentTree.xpath('//html/body/div/span/text()')
# print(buyers)
# print(prices)




read_loadsim_cmm = 'std_loadsim_mpss_htc_8996_poser.cmm'
write_loadsim_cmm = 'std_loadsim_mpss_htc_8996_poser_out.cmm'

read_loadsyms_cmm = 'std_loadsyms_mpss_poser.cmm'
write_loadsyms_cmm = 'std_loadsyms_mpss_poser_out.cmm'

Radio_release_root = r'\\10.116.56.36\Release'
T32_full_path = r'D:\M1\T32_D\bin\windows64\t32mqdsp6'
#Radio_release_root = r'C:\Users\poser_lin\Desktop\QXDM_log'
#BIN_file_location = r'\\wsd-abs-w2b-2\David\S1_M1_ITS\268\Ramdump_HT6560300026_20160517035548\DDRCS0.bin'
#Radio_version = '8996-011002-1605051809'

BIN_file_location = input("Plz input DDRCS0.BIN: \r\n")
Radio_version = input("Plz input Radio version: ")


Radio_str= Radio_version.split("-")
ELF_file_location = 0
#========================================================== 
# Function declarification
#==========================================================    
#Define the Search elf based on provide radio version
def search_elf(search_dir, Radio_version):
    for dirPath, dirNames, fileNames in os.walk(search_dir):   
        for x in fileNames:
            if fnmatch.fnmatch(x, '*'+Radio_version+'*.img'):                
                for elf in os.listdir(dirPath):
                    if fnmatch.fnmatch(elf, 'M*.elf'):
                        ELF_file = os.path.join(dirPath, elf)
                        print('Match ELF is \r\n %s' %ELF_file)
                        return ELF_file

#Define the update_cmm function for update correct cmm script
def update_cmm(read_cmm, write_cmm, replace_target, replace_object):
    with open(write_cmm, 'w') as output_file, open(read_cmm, 'r') as input_file:
        for line in input_file:
            output_file.write(line.replace(replace_target, replace_object)) 

            
# Search dir by release ver
if len(Radio_str) == 3: # full radio version, parser & speed up search by release version
    for dir_1 in os.listdir(Radio_release_root): 
        if re.search(Radio_str[1], dir_1):
            new_path = os.path.join(Radio_release_root, dir_1)
            for dir_2 in os.listdir(new_path):
                if re.search(Radio_str[2], dir_2):
                    new_path = os.path.join(new_path, dir_2)
                    ELF_file_location = search_elf(new_path, Radio_version)
            

#if Fail, Search all dir from root, support partial Radio ver search
if ELF_file_location == 0:
    print('Full search from root dir due to partial Radio_ver')            
    ELF_file_location = search_elf(Radio_release_root, Radio_version)
        
if ELF_file_location == 0:
    print('Fail to find ELF')
else:
    update_cmm(read_loadsim_cmm,write_loadsim_cmm, 'BIN_location',BIN_file_location)
    update_cmm(read_loadsyms_cmm,write_loadsyms_cmm, 'ELF_location_HTC',ELF_file_location)    
    os.system(T32_full_path + ' -s' +write_loadsim_cmm)         
            
 
