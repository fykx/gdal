import os
os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'
#os.environ['GDAL_DATA'] = r'/public/home/mfeng/anaconda3/envs/geo/share'

def listdatas_1(pathin):
    '''用于查找边界栅格单元'''
    import os

    _datas = []
    _names = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _names.append(_file.split("_")[0])
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []               
    for _name in list(set(_names)):
        for _data in _datas:
            if _data.split('/')[-1].split('_')[0] == _name:
                _mosaic_datas.append(_data)
                break
    return _mosaic_datas

def intersectornot(r_data, shp):
    '''判断影像是否与矢量边界相交'''
    from osgeo import gdal,ogr,osr

    _in_ds = gdal.Open(r_data)
    _in_band = _in_ds.GetRasterBand(1)#波段索引从1开始
    _adfGeoTransform = _in_ds.GetGeoTransform()

    _xsize = _in_band.XSize#列
    _ysize = _in_band.YSize#行
    
    #左上角
    _lon_0 = _adfGeoTransform[0] + range(_xsize)[0] * _adfGeoTransform[1] + range(_ysize)[0] * _adfGeoTransform[2]
    _lat_0 = _adfGeoTransform[3] + range(_xsize)[0] * _adfGeoTransform[4] + range(_ysize)[0] * _adfGeoTransform[5]

    #右上角
    _lon_1 = _adfGeoTransform[0] + range(_xsize)[0] * _adfGeoTransform[1] + range(_ysize)[-1] * _adfGeoTransform[2]
    _lat_1 = _adfGeoTransform[3] + range(_xsize)[0] * _adfGeoTransform[4] + range(_ysize)[-1] * _adfGeoTransform[5]

    #左下角
    _lon_2 = _adfGeoTransform[0] + range(_xsize)[-1] * _adfGeoTransform[1] + range(_ysize)[0] * _adfGeoTransform[2]
    _lat_2 = _adfGeoTransform[3] + range(_xsize)[-1] * _adfGeoTransform[4] + range(_ysize)[0] * _adfGeoTransform[5]

    #右下角
    _lon_3 = _adfGeoTransform[0] + range(_xsize)[-1] * _adfGeoTransform[1] + range(_ysize)[-1] * _adfGeoTransform[2]
    _lat_3 = _adfGeoTransform[3] + range(_xsize)[-1] * _adfGeoTransform[4] + range(_ysize)[-1] * _adfGeoTransform[5]
    
    #写入几何、属性
    _ring = ogr.Geometry(ogr.wkbLinearRing)
    _ring.AddPoint(_lon_0, _lat_0)
    _ring.AddPoint(_lon_1, _lat_1)
    _ring.AddPoint(_lon_3, _lat_3)
    _ring.AddPoint(_lon_2, _lat_2)
    _ring.AddPoint(_lon_0, _lat_0)
    _poly = ogr.Geometry(ogr.wkbPolygon)
    _poly.AddGeometry(_ring)

    _shp_ds = ogr.Open(shp, 0)
    _in_lyr = _shp_ds.GetLayer(0)
    _shp_feature = _in_lyr.GetNextFeature()
    _shp_geometry = _shp_feature.geometry()
    return _shp_geometry.Contains(_poly)

def intersect_datas(pathin, shp):
    datas = listdatas_1(pathin)
    intersect_datas = []
    for r_data in datas:
        if intersectornot(r_data, shp) == False:
            intersect_datas.append(r_data.split('/')[-1].split('.')[0].split('_')[0])
    return intersect_datas

def listdatas_2(pathin):
    '''用于查所有数据'''
    import os

    _datas = []
    for _root, _dirs, _files in os.walk(pathin):
        _datas_i = []
        if len(_files) != 0:
            for _file in _files:
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas_i.append(_vv)
        _datas_i.sort()
        if len(_datas_i) != 0:
            _datas.append(_datas_i)
    return _datas

def clip(data, mask, pathout, split_str):
    '''影像裁剪'''
    import os
    from osgeo import gdal,ogr,osr

    path_data = pathout + data.split(split_str)[-1]
    pathout_1 = path_data.replace('/' + path_data.split('/')[-1],'')

    if os.path.isdir(pathout_1):
        pass
    else:
        os.makedirs(pathout_1)

    os.system('gdalwarp -srcnodata -99.0 -dstnodata -99.0 -cutline {} {} {}'.format(mask, data, path_data))
    return

def divide(datas, n):
    '''进程分割'''
    mpi_datas = {}
    step = len(datas)//n
    for i in range(n):
        if i < n-1:
            mpi_data = datas[i*step:(i+1)*step]
            mpi_datas[i] = mpi_data
        else:
            mpi_data = datas[i*step:]
            mpi_datas[i] = mpi_data

    j = 0
    while len(mpi_datas[n-1]) > step and j < n-1:
        mpi_datas[j].append(mpi_datas[n-1][-1])
        mpi_datas[n-1].remove(mpi_datas[n-1][-1])
        j = j + 1
    
    mpi_datas_out = []
    for mpi_data_out in mpi_datas.values():
        mpi_datas_out.append(mpi_data_out)
    return mpi_datas_out

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    parser.add_argument('-m', '--mask', type=str, help='mask', required=True)# 掩膜
    parser.add_argument('-s', '--split_str', type=str, help='split_string', required=True)# 用于分割的字符串
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    datas = listdatas_2(args.input)
    inter_datas = intersect_datas(args.input, args.mask)

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for i in mpi_data_divide:
        for j in i:
            if j.split('/')[-1].split('.')[0].split('_')[0] in inter_datas:
                print(j)
                clip(j, args.mask, args.output, args.split_str)
    return

if __name__ == '__main__':
    main()
# mpiexec -n 1 python clip.py -i /mnt/e/r_tcc/h1557 -o /mnt/e/r_tcc/out -m /mnt/e/r_tcc/ne_shp/NE_WGS1984.shp -s r_tcc -n 1
# mpiexec -n $NP -hostfile $PBS_NODEFILE python clip.py -i /public/home/mfeng/jwang/forest/northeast/tcc/data -o /public/home/mfeng/jwang/forest/northeast/tcc/clip_data -m /public/home/mfeng/jwang/forest/northeast/tcc/ne_shp/NE_WGS1984.shp -s tcc -n $NP


