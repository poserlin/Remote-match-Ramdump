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
import shutil


from lxml import etree
from lxml import html


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

#Define the Remote Search                         
def search_elf_remote(Radio_release_root, Radio_str):   
    print('>>> Searching Remotely......', end='')
    # Search remote dir by release ver
    if len(Radio_str) == 3: # full radio version, parser & speed up search by release version
        for dir_1 in os.listdir(Radio_release_root): 
            if re.search(Radio_str[1], dir_1):
                new_path = os.path.join(Radio_release_root, dir_1)
                for dir_2 in os.listdir(new_path):
                    if re.search(Radio_str[2], dir_2):
                        new_path = os.path.join(new_path, dir_2)
                        ELF_file_remote_location = search_elf(new_path, Radio_version)                        
                        
    #if Fail, Search all dir from root, support partial Radio ver search
    if ELF_file_remote_location == 0:
        #print('Full search from root dir due to partial Radio_ver')            
        ELF_file_remote_location = search_elf(Radio_release_root, Radio_version)                    
        
    #if Found, copy ELF from remote server to Temp_Elf_folder
    if ELF_file_remote_location != 0:    
        ELF_file_rename = os.path.splitext(os.path.basename(ELF_file_remote_location))[0]+'_'+Radio_str[2]+os.path.splitext(os.path.basename(ELF_file_remote_location))[1]
        Local_ELF_file_location = os.path.join(Temp_Elf_folder, ELF_file_rename)
        print('>>>>>>Found, Copy file from SSD server......')
        shutil.copy(ELF_file_remote_location, Local_ELF_file_location)
        
        
        #checking the file size, if match, add _fin in the file name.
        if os.path.getsize(Local_ELF_file_location) != os.path.getsize(ELF_file_remote_location):
            return 0
        else:
            print('>>>>>>Finish copying......')
            os.replace(Local_ELF_file_location, os.path.splitext(Local_ELF_file_location)[0]+'_fin'+os.path.splitext(Local_ELF_file_location)[1])
            return Local_ELF_file_location

    
#Define the local Search
def search_elf_local(search_dir, Radio_version):
    print('>>> Searching Locally......', end='')
    ELF_file = 0
    # Full radio version
    if len(Radio_version) == 3:
        Radio_version_part = Radio_version[2]
    else:
        Radio_version_part = Radio_version[0]
        
    for dirPath, dirNames, fileNames in os.walk(search_dir):   
        for x in fileNames:
            if fnmatch.fnmatch(x, '*'+Radio_version_part+'_fin.elf'):
                ELF_file = os.path.join(search_dir, x)
                print('Match ELF locally in  \r\n %s' %ELF_file)
                return ELF_file 
    print('Not found locally')         
    return 0

        
#Define the update_cmm function for update correct cmm script
def update_cmm(read_cmm, write_cmm, replace_target, replace_object):
    with open(write_cmm, 'w') as output_file, open(read_cmm, 'r') as input_file:
        for line in input_file:
            output_file.write(line.replace(replace_target, replace_object)) 





#========================================================== 
# Variable declarification
#==========================================================
cmm_path = r'\common\Core\tools\cmm\common\msm8996\\'

Codebase_root_folder = r'D:\codebase\8996\8996_AND_LA_1.9_11701_UMTS_24.00_0624_3852742_160'

read_loadsim_cmm = r'std_loadsim_mpss_htc_8996_poser.cmm'
write_loadsim_cmm = r'std_loadsim_mpss_htc_8996_poser_out.cmm'

read_loadsyms_cmm = r'std_loadsyms_mpss_poser.cmm'
write_loadsyms_cmm = r'std_loadsyms_mpss_poser_out.cmm'

read_loadsim_cmm_all = Codebase_root_folder+cmm_path+read_loadsim_cmm
write_loadsim_cmm_all = Codebase_root_folder+cmm_path+write_loadsim_cmm

read_loadsyms_cmm_all = Codebase_root_folder+cmm_path+read_loadsyms_cmm
write_loadsyms_cmm_all = Codebase_root_folder+cmm_path+write_loadsyms_cmm


Radio_release_root = r'\\10.116.56.36\Release'
T32_full_path = r'D:\M1\T32_D\bin\windows64\t32mqdsp6'
Temp_Elf_folder = r'D:\M1\dump\ELF_temp'




ELF_file_location = 0
#Radio_release_root = r'C:\Users\poser_lin\Desktop\QXDM_log'
#BIN_file_location = r'\\wsd-abs-w2b-2\David\S1_M1_ITS\268\Ramdump_HT6560300026_20160517035548\DDRCS0.bin'
#Radio_version = '8996-011002-1605051809'



#========================================================== 
# Main function
#==========================================================  

BIN_file_location = input("Plz input DDRCS0.BIN: \r\n")
Radio_version = input("Plz input Radio version: ")

Radio_str= Radio_version.split("-")

# Search internal ELF first         
ELF_file_location = search_elf_local(Temp_Elf_folder, Radio_str)
                        
# If local Search fail, Search remote dir by release ver
if ELF_file_location == 0:
    ELF_file_location = search_elf_remote(Radio_release_root, Radio_str)
  
if ELF_file_location == 0:
    print('Fail to find ELF')
else:
    update_cmm(read_loadsim_cmm_all, write_loadsim_cmm_all, 'BIN_location',BIN_file_location)
    update_cmm(read_loadsyms_cmm_all, write_loadsyms_cmm_all, 'ELF_location_HTC',ELF_file_location)    
    os.system(T32_full_path + ' -s' +write_loadsim_cmm_all)         
            
 
