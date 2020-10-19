# -*- coding: utf-8 -*-
import xlrd
import openpyxl
import pandas as pd 
import os
import string
import csv
import sys


data = xlrd.open_workbook('diff.xlsx')
data.sheet_names()
print(str(data.sheet_names()))
table = data.sheet_by_index(0)
col1 = (table.col_values(0))
col2 = (table.col_values(1))
print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))
# col2.strip()
for i in range(len(col1)):
    col1[i] = str(col1[i]).strip()
for i in range(len(col2)):
    col2[i] = str(col2[i]).strip()
diff = []
# print(col2)

for i in col1:
    # print(i)
    # print(type(col1))
    # print(type(col2))
    # break
    if i not in col2:
        # print(i)
        diff.append(i)


pf = pd.DataFrame(diff)
file_path = pd.ExcelWriter('after-diff.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=False)
file_path.save()

# with open ('test.csv', 'w', newline='',encoding='utf-8') as f:
#     writer = csv.writer(f)
#     for i in diff:
#         writer.writerow([i])

# data = xlrd.open_workbook(sys.argv[1])
# data.sheet_names()
# print(str(data.sheet_names()))
# table = data.sheet_by_index(0)
# col1 = (table.col_values(0))
# col2 = (table.col_values(1))
# col3 = (table.col_values(2))
# col4 = (table.col_values(3))
# col5 = (table.col_values(4))
# col6 = (table.col_values(5))
# values = []
# # for row in range(col2):
# #     for col in range()
# print(col2)
# print(len(col2))
# lists = ['3/4 compression pants men ', '3 4 leggings men ', '3 4 mens tights ']

# words = [raw_word.strip(string.punctuation).lower() for raw_word in lists.split()]
# words_index = set(words)


