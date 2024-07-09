import pandas as pd
import json
import math
import os
import csv
x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率

def bd09togcj02(lng,lat):
    x = lng -0.0065;
    y = lat-0.006;
    z=math.sqrt(x*x+y*y)- 0.00002 * math.sin(y * x_pi);
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi);
    return[z * math.cos(theta),z * math.sin(theta)]


def gcj02towgs84(lng, lat):
    """
    GCJ02(⽕星坐标系)转GPS84
    :param lng:⽕星坐标系的经度
    :param lat:⽕星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    # radlat = lat / 180.0 * pi
 
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]
 
 
def transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
 
 
def transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret
 
 
def out_of_china(lng, lat):
    """
判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    if lat < 0.8293 or lat > 55.8271:
        return True
    return False
 
 
if __name__ == '__main__':
    # 数据输出路径
    path = r"D:/桌面/增/"
    # 读取Excel⽂件
    df = pd.read_excel(r"D:/桌面/增/14.xlsx")
    if not os.path.exists(path):
        os.mkdir(path)
    # 输出转换后⽣成csv的⽂件名称
    with open(path + "完成转换坐标结果.csv", "w", newline="") as file:
        writter = csv.writer(file)
        # 经度84和纬度84是转换后的数值，名称是原表中保留的字段
        writter.writerow(["经度", "纬度", "id"])
        for index, row in df.iterrows():
            # lng和lat是原表中存储经度、纬度的字段
            j = bd09togcj02(row["lon"], row["lat"])
            i = gcj02towgs84(j[0], j[1])
            writter.writerow([row["id"],row["name"],row["location"],row["adcode"],row["address"],row["tel"],i[0], i[1]])
        file.close()
    print("坐标转换完毕")
 
 