import os
os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'

def listdatas(pathin):
    '''列出同年份数据'''
    import os

    _datas = []
    _years = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _vv = None
                if _file.endswith('_dat.tif') and _file.split('_')[1] != 'avg':
                    _years.append(_file.split("_")[1])
                    _vv = os.path.join(_root, _file)
                    _datas.append(_vv)

    _mosaic_datas = []
    for _year in list(set(_years)):
        _mosaic_data = []
        for _data in _datas:
            if _data.split('/')[-1].split('_')[1] == _year:
                _mosaic_data.append(_data)
        _mosaic_datas.append(_mosaic_data)
    return _mosaic_datas

def read_hist_mean(datalist, taskshp, ne):
    import os
    from osgeo import gdal,ogr,osr
    import numpy as np

    ds_mask = ogr.Open(ne, 0)
    lyr_mask = ds_mask.GetLayer(0)
    mask_feature = lyr_mask.GetNextFeature()
    mask_geometry = mask_feature.geometry()

    ds = ogr.Open(taskshp, 0)
    lyr = ds.GetLayer(0)

    a = []# 需要裁剪的栅格
    b = []# 所有相交的栅格

    for feat in lyr:
        task_geometry = feat.geometry()
        if mask_geometry.Intersects(task_geometry) == True:
            b.append(feat.GetField('tag'))
            if mask_geometry.Contains(task_geometry) == False:
                a.append(feat.GetField('tag'))

    year = int(datalist[0].split('/')[-1].split('_')[1].replace('y',''))
    mean_value = 0
    fykx_array = np.array([0 for i in range(101)])

    for data in datalist:
        if data.split('/')[-1].split('_')[0] in b:
            if data.split('/')[-1].split('_')[0] in a:
                mask_ds = gdal.Warp('', data, format='MEM', cutlineDSName=ne, dstNodata=255)
                in_mask_band = mask_ds.GetRasterBand(1)
                in_mask_data = in_mask_band.ReadAsArray().astype(float)# 求均值
                in_mask_data_array = np.ma.masked_where(in_mask_data>100.0, in_mask_data)
                fykx_mean_value = np.mean(in_mask_data_array)# 栅格均值
                hist = in_mask_band.GetHistogram(0, 100, 101, include_out_of_range=False, approx_ok=False)
                hist_array = np.array(hist)
                del mask_ds
            else:
                ds = gdal.Open(data)
                band = ds.GetRasterBand(1)
                data_array = band.ReadAsArray().astype(float)# 求均值
                data_mask_array = np.ma.masked_where(data_array>100.0, data_array)
                fykx_mean_value = np.mean(data_mask_array)# 栅格均值
                hist = band.GetHistogram(0, 100, 101, include_out_of_range=False, approx_ok=False)
                hist_array = np.array(hist)
                del ds
            mean_value = mean_value + fykx_mean_value
            fykx_array = fykx_array + hist_array
            
    return year, mean_value/len(b), fykx_array

def draw_hist(datalist, pathout, taskshp, ne):
    from matplotlib import pyplot as plt
    from matplotlib.pyplot import MultipleLocator
    import numpy as np

    x = [x for x in range(101)]
    x_array = np.array(x)

    year, mean_value, fykx_array = read_hist_mean(datalist, taskshp, ne)
    print(year,',',mean_value)

    fig, ax = plt.subplots(1,1,figsize=(6,4))
    plt.bar(x_array, fykx_array, align =  'center')

    plt.title(str(year) + ' ' + 'Histogram')
    plt.ylabel('Frequency')
    plt.xlabel('Pixel Value')
    fig.savefig(pathout + '/' + str(year) + '.png', dpi=300, bbox_inches='tight')
    plt.close()
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
    parser.add_argument('-ta', '--task', type=str, help='task', required=True)# task_shp
    parser.add_argument('-ne', '--northeast', type=str, help='northeast', required=True)# northeast
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    datas = listdatas(args.input)

    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for datalist in mpi_data_divide:
        draw_hist(datalist, args.output, args.task, args.northeast)
    return

if __name__ == '__main__':
    main()