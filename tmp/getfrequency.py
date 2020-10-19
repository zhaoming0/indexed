#--*-- coding:utf-8 --*--
import xlrd
import os
from collections import Counter
import csv
import sys
import pandas as pd 


filename='1.xlsx'
print(filename)        
data = xlrd.open_workbook(filename)
data.sheet_names()
print("sheets：" + str(data.sheet_names()))
table = data.sheet_by_index(0)

print("总行数：" + str(table.nrows))
print("总列数：" + str(table.ncols))
# print("整行值：" + str(table.row_values(0)))
# print("整列值：" + str(table.col_values(0)))
result = ((table.col_values(0)))

print(len(result))
#1.xlsx
values = []
for i in range(len(result)):
    sublist = str(result[i]).rstrip().split(' ')
    for b in range(len(sublist)):
        values.append(sublist[b])
# print(values)
counts = Counter(values)
# print(counts)

pf = pd.DataFrame(list(counts.items()))
file_path = pd.ExcelWriter('getfrequency.xlsx')
pf.to_excel(file_path,encoding='utf-8',index=False)
file_path.save()

