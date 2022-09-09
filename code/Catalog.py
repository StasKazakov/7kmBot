# This modul make list of all shops
import openpyxl
import os

path = '../photo/'
catalog = open("../" + "catalog.txt", "w+", encoding='utf-8')

# Rename folders

shop = openpyxl.open("../shops.xlsx", read_only=True)
sheet = shop.active

dict_shop = {}
for namb in range(1, sheet.max_row + 1):
    key = (sheet['A' + str(namb)].value)
    dict_shop[key] = (sheet['B' + str(namb)].value)

with os.scandir(path) as files:
    shops = [file.name for file in files if file.is_dir()]

for name in shops:
    n = dict_shop.get(name)
    if n != None:
        os.chdir(path)
        os.rename(name, dict_shop[name])

# Scanning all folder, search folders

with os.scandir(path) as files:
    shops = [file.name for file in files if file.is_dir()]

# Name of folders print in TXT

for el in shops:
    catalog.write(el + '\n')

catalog.close()
