'''
Descripttion: 读取csv文件转为shp
version: 0.1
Author: Jianbang Wang
Date: 2021-03-01
'''

def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.csv'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def readcsv(data):
    import pandas as pd

    data_name = data.split('/')[-1].split('.')[0]# 获取数据名称（不包括后缀）

    df = pd.read_csv(data, header=0)# header=0表示使用数据列索引

    columns = df.columns # 获取列索引

    data_list = df.values.tolist()# 获取df的values，并将每一行转为list

    #for row in df.itertuples(index=True, name='Pandas'):# 遍历df每一行
        #print(getattr(row, "lon"), getattr(row, "lat"))
    return data_name, columns, data_list

def toshp(data_name, columns, data_list, pathout):
    from osgeo import gdal, ogr, osr

    '''创建DataSource，并添加图层'''
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)# WGS84
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(pathout + '/' + data_name + '.shp')
    lyr = ds.CreateLayer(data_name, sr, ogr.wkbPoint)

    '''新建字段'''
    for col in columns:
        fld = ogr.FieldDefn(col, ogr.OFTReal)
        fld.SetWidth(20)
        fld.SetPrecision(7)
        lyr.CreateField(fld)

    feat = ogr.Feature(lyr.GetLayerDefn())

    '''写入几何和属性'''
    for j in data_list:
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(j[3]), float(j[4]))
        feat.SetGeometry(point)# 写入几何
        for q in range(len(j)):
            feat.SetField(q,j[q])# 写入属性
        lyr.CreateFeature(feat)
    return


def main():
    pathin = r'/public/home/mfeng/jwang/work_tcc/test_1/china/file01/scene01/comp01/change0a/0301/data'
    pathout = r'/public/home/mfeng/jwang/work_tcc/test_1/china/file01/scene01/comp01/change0a/0301/out/1_point'
    datas = listdatas(pathin)
    for data in datas:
        data_name, columns, data_list = readcsv(data)
        print(data_name)
        toshp(data_name, columns, data_list, pathout)
    return


if __name__ == "__main__":
    main()


