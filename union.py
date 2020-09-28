'''列出数据'''
def listdatas(pathin):
    import os
    _a = []
    _datas = os.listdir(pathin)
    for _i in _datas:
        if _i[-4:] == '.shp':
            _fn_i = pathin + '/' + _i
            _a.append(_fn_i)
    return _a

def union(datalist, pathout, geom_type):
    from osgeo import gdal,ogr,osr
    
    #输出投影
    _out_srs = osr.SpatialReference()
    _out_srs.ImportFromEPSG(4326)

    #建立新数据集
    _driver = ogr.GetDriverByName('ESRI Shapefile')
    _ds_0 = _driver.CreateDataSource(pathout + '/' + 'proj_' + 'out.shp')
    _out_lyr = _ds_0.CreateLayer('out', _out_srs, geom_type)

    #添加字段
    _fld = ogr.FieldDefn('name', ogr.OFTString)
    _fld.SetWidth(100)
    _out_lyr.CreateField(_fld)

    #创建空要素
    _out_feat = ogr.Feature(_out_lyr.GetLayerDefn())

    for _fn in datalist:
        _ds = ogr.Open(_fn, 0)#第二个参数0表示以只读方式打开文件
        _in_lyr = _ds.GetLayer(0)
        #写入几何、属性
        for _in_feat in _in_lyr:
            _geom = _in_feat.geometry()
            _out_feat.SetGeometry(_geom)
            for _i in range(_in_feat.GetFieldCount()):
                _out_feat.SetField(_i, _in_feat.GetField(_i))
            _out_lyr.CreateFeature(_out_feat)
    return

def main():
    from osgeo import gdal,ogr,osr
    pathin = r'/mnt/e/r1/out/shp'
    pathout = r'/mnt/e/r1/out/union'
    datalist = listdatas(pathin)
    geom_type = ogr.wkbPolygon
    union(datalist, pathout, geom_type)

if __name__ == '__main__':
    main()