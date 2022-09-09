# This module make hash for all Catalog

import os
from Functions import CalcImageHash
import shutil

# Read list of shops

path = '../photo/'
with open("../catalog.txt", encoding='utf-8') as f:
    clist = f.read().splitlines()
current_folder = 0

# Make hashlist in every shop

while current_folder < len(clist):
    pathn = '../shops/'
    path_img = '../photo/' + clist[current_folder] + '/'
    file = open(pathn + clist[current_folder] + '.txt', "w+", encoding='utf-8')
    img = os.listdir(path_img)
    current_file = 0
    am = len(img)

# Count hash for shop.

    while current_file < am:
        hash1 = CalcImageHash(path_img + img[current_file])
        file.write(hash1 + '\n')
        current_file += 1
    file.close()
    current_folder += 1

# Delete all folders with foto

current_folder = 0
while current_folder < len(clist):
    dir_path = '../photo/'
    shutil.rmtree(dir_path + clist[current_folder] + '/')
    current_folder += 1