'''
@Descripttion: 判断参与镶嵌的影像，输到.sh文件，并执行
@version: 0.1
@Author: Jianbang Wang
@Date: 2020-07-24 17:03:53
'''

def listdatas(pathin):
    import os

    _datas = []
    _years = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _years.append(_file.split("_")[2])
                _vv = None
                if _file.endswith('_dat.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []               
    for _year in list(set(_years)):
        _mosaic_data = []
        for _data in _datas:
            if _data.split('\\')[-1].split("_")[2] == _year:
                _mosaic_data.append(_data)
        _mosaic_datas.append(_mosaic_data)
    return _mosaic_datas


def filter(pathin_data, mask_data, pathout):
    from osgeo import ogr,gdal

    #保证程序在出现问题时报错
    ogr.UseExceptions()

    ds_0 = ogr.Open(mask_data, 0)
    lyr_0 = ds_0.GetLayer(0)

    feat = lyr_0.GetNextFeature()
    syh = feat.geometry().Clone()

    ds_1 = ogr.Open(pathin_data, 1)
    lyr_1 = ds_1.GetLayer(0)

    lyr_1.SetSpatialFilter(syh)

    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(pathout + '/' + '2.shp')
    out_lyr = ds.CreateLayer('2', lyr_0.GetSpatialRef(), ogr.wkbPoint)

    out_lyr.CreateFields(lyr_1.schema)

    out_defn = out_lyr.GetLayerDefn()
    out_feat = ogr.Feature(out_defn)

    a = []

    for feat in lyr_1:
        geom = feat.geometry()
        out_feat.SetGeometry(geom)
        for i in range(feat.GetFieldCount()):
            value = feat.GetField(i)
            out_feat.SetField(i, value)
            a.append(value.split("_")[0])
        out_lyr.CreateFeature(out_feat)
    del ds
    return list(set(a))

def mian(pathin_data, mask_data, pathout, pathin):
    #import os

    datas = listdatas(pathin)
    filter_datas = filter(pathin_data, mask_data, pathout)

    nn = pathout + '/' + 'mysh.sh'
    f = open(nn,'w')

    for i in datas:
        

        mossic_datas = []
        f.write('gdal_merge.py -o {} '.format(pathout + '/' + i[0].split('\\')[-1].split('_')[2] + '.tif'))
        for j in i:
            #print(j)
            if j.split('/')[-1].split('_')[0] in filter_datas:
                mossic_datas.append(j)
                f.write('{} '.format(j))
        f.write('\n')
    f.close()

    #os.system('cd {}'.format(pathout))
    #os.system('chmod +x mysh.sh')
    #os.system('./mysh.sh')
    return


if __name__ == "__main__":
    pathin_data = r'/home/forest/ne/out/1.shp'
    mask_data = r'/home/forest/ne/dxal_shp/dxal.shp'
    pathout = r'/home/forest/ne/out'
    pathin = r'/home/forest/ne/data'
    mian(pathin_data, mask_data, pathout, pathin)
