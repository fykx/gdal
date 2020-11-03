def listdatas(pathin):
    import os

    _datas = []
    for _root, _dirs, _files in os.walk(pathin):
        _datas_i = []
        if len(_files) != 0:
            for _file in _files:
                _vv = None
                if _file.endswith('_dat.tif') and _file.split('_')[1] != 'avg':
                   _vv = os.path.join(_root, _file)
                   _datas_i.append(_vv)
        _datas_i.sort()
        if len(_datas_i) != 0:
            _datas.append(_datas_i)
    return _datas

def divide(datas, n):
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


def mean_raster(datas, pathout):
    from osgeo import gdal
    import numpy as np

    datas.sort()

    in_ds = gdal.Open(datas[0])
    in_band = in_ds.GetRasterBand(1)
    xsize = in_band.XSize
    ysize = in_band.YSize

    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + datas[0].split('/')[-1].split('.')[0].split('_')[0] + '.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    para_0 = np.zeros(shape=(ysize, xsize))

    for data in datas:
        print(data.split('/')[-1])
        ds = gdal.Open(data)
        band = ds.GetRasterBand(1)
        data_array = band.ReadAsArray().astype(float)
        data_mask_array = np.where(data_array==-99.0, np.nan, data_array)
        para_0 = para_0 + data_mask_array
    out_array = para_0/len(datas)
    out_array = np.where(np.isnan(out_array), -99.0, out_array)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_array)
    #out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    datas = listdatas(args.input)
    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for mpi_data in mpi_data_divide:
        mean_raster(mpi_data, args.output)
    return

if __name__ == "__main__":
    main()
    # mpiexec -n 60 python Interpolation.py -i /public/home/mfeng/work/test/forest/pangyong/phase2/ne/forest/file12/scene04/comp01/data -o /public/home/mfeng/jwang/forest/northeast/tcc -s comp01 -n 60
