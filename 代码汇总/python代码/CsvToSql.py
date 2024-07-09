import csv
# 读取 csv 文件
with open("G:/大三下/GIS 实践/14.csv", 'r', encoding='utf-8') as f:
reader = csv.DictReader(f)
data = [row for row in reader]
# 转换数据格式
output = []
for item in data:
lon, lat = item['lon'], item['lat']
output.append("INSERT INTO coordinates (lon, lat) VALUES ({}, {});".format(lon, lat))
# 输出为 txt 文件
with open('output.txt', 'w', encoding='utf-8') as f:
f.write('\n'.join(output))