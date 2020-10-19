import os
import string
import csv

filename = []
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        filename.extend(files)
file_name('.')

with open ('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    for i in filename:
        if i.endswith('.png'):
            imagename = (i.replace('-', '/').replace('_', ' ').strip('.png').rstrip(string.digits))
            imagenum = (i.strip('.png').split('_'))[-1]
            writer.writerow([imagename,imagenum])
