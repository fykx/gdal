#import os
#os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'
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
    '''判断影像是否在矢量范围内'''
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
            intersect_datas.append(r_data.replace('/' + r_data.split('/')[-1],''))
    return intersect_datas


def delte(data):
    '''影像删除'''
    import os

    os.system('rm -rf {}'.format(data))
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
    parser.add_argument('-m', '--mask', type=str, help='mask', required=True)# 掩膜
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    inter_datas = intersect_datas(args.input, args.mask)

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    mpi_datas = divide(inter_datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for data in mpi_data_divide:
        print(data)
        delte(data)
    return

if __name__ == '__main__':
    main()
# mpiexec -n 1 python delete.py -i /mnt/e/r_tcc/h1557 -m /mnt/e/r_tcc/ne_shp/NE_WGS1984.shp -n 1
# mpiexec -n $NP -hostfile $PBS_NODEFILE python delete.py -i /public/home/mfeng/jwang/forest/northeast/tcc/data -m /public/home/mfeng/jwang/forest/northeast/tcc/ne_shp/NE_WGS1984.shp -n $NP