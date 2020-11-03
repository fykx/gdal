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

def mean_raster(datas, pathout, para_width, para_height):
    from osgeo import gdal
    import numpy as np
    import math

    datas.sort()

    in_ds = gdal.Open(datas[0])
    in_band = in_ds.GetRasterBand(1)
    #nodata = in_band.GetNoDataValue()
    xsize = in_band.XSize#列
    ysize = in_band.YSize#行
    
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + datas[0].split('/')[-1].split('_')[0] + '.tif', xsize, ysize, 1, gdal.GDT_Float32)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    out_data = np.zeros(shape=(ysize, xsize))
    progress = 0
    for i in range(math.ceil(xsize/para_width)):#列
        for j in range(math.ceil(ysize/para_height)):#行
            print(round(progress/(math.ceil(xsize/para_width)*math.ceil(ysize/para_height))*100,2),'%')
            progress = progress + 1
            datas_array = []
            for data in datas:
                ds = gdal.Open(data)
                band = ds.GetRasterBand(1)
                if (i+1)*para_width <= xsize and (j+1)*para_height <= ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, para_width, para_height).astype(float)
                    #f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(data_array)

                elif (i+1)*para_width > xsize and (j+1)*para_height <= ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, xsize - i*para_width, para_height).astype(float)
                    #f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(data_array)

                elif (i+1)*para_width <= xsize and (j+1)*para_height > ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, para_width, ysize - j*para_height).astype(float)
                    #f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(data_array)

                elif (i+1)*para_width > xsize and (j+1)*para_height > ysize:
                    data_array = band.ReadAsArray(i*para_width, j*para_height, xsize - i*para_width, ysize - j*para_height).astype(float)
                    #f_array = np.where(np.isnan(data_array), -99.0, data_array)
                    datas_array.append(data_array)
                del ds

            height, width = data_array.shape

            for x in range(width):#遍历列
                for y in range(height):#遍历行
                    value_list = []
                    for array in datas_array:
                        if array[y, x] == -99.0:
                            pass
                        else:
                            value_list.append(array[y,x])
                    if len(value_list) == 0:
                        out_data[j*para_height+y, i*para_width+x] = -99.0
                    else:
                        out_data[j*para_height+y, i*para_width+x] = np.mean(value_list)

    out_band = out_ds.GetRasterBand(1)
    out_band.FlushCache()
    out_band.WriteArray(out_data)
    out_band.SetNoDataValue(-99.0)
    out_band.ComputeStatistics(False) 
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
    parser.add_argument('-wi', '--width', type=int, help='width', required=True)# 列（宽）
    parser.add_argument('-he', '--height', type=int, help='height', required=True)# 行（高）
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    datas = listdatas(args.input)

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for i in mpi_data_divide:
        mean_raster(i, args.output, args.width, args.height) 
    return

if __name__ == '__main__':
    main()

# mpiexec -n 4 python mean.py -i /mnt/e/r_tcc/tcc_new -o /mnt/e/r_tcc/out -wi 400 -he 400 -n 4
# mpiexec -n $NP -hostfile $PBS_NODEFILE python mean.py -i /public/home/mfeng/jwang/forest/northeast/tcc/tcc_new -o /public/home/mfeng/jwang/forest/northeast/out/mean/1 -wi 200 -he 200 -n $NP
# mpiexec -n $NP -hostfile $PBS_NODEFILE python clip.py -i /public/home/mfeng/jwang/forest/northeast/tcc/data -o /public/hom