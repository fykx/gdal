import os
#os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'

def read(data_txt):
    '''读出无值栅格'''
    import re

    a = []
    f = open(data_txt, 'r')
    #f.readline()
    for line in f.readlines():
        a.append(re.split(',', line.strip())[0].split(' ')[-1].split('/')[-1].split('.')[0])
    f.close()
    return a

def listdatas(pathin, data_txt):
    '''列出同年份数据'''
    import os

    a = read(data_txt)

    _datas = []
    _years = []
    for _root, _dirs, _files in os.walk(pathin):
        if len(_files) != 0:
            for _file in _files:
                _years.append(_file.split("_")[1])
                _vv = None
                if _file.endswith('.tif'):
                   _vv = os.path.join(_root, _file)
                   _datas.append(_vv)

    _mosaic_datas = []
    for _year in list(set(_years)):
        _mosaic_data = []
        for _data in _datas:
            if _data.split('/')[-1].split('_')[1] == _year and _data.split('/')[-1].split('_')[0] not in a:
                _mosaic_data.append(_data)
        _mosaic_datas.append(_mosaic_data)
    return _mosaic_datas

def mosaic(datalist, pathout):
    '''影像镶嵌'''
    import os
    from osgeo import gdal

    year = datalist[0].split('/')[-1].split('_')[1]

    datas_str = ''
    for i in range(len(datalist)):
        datas_str = datas_str + ' ' + datalist[i]
    os.system('gdalwarp -srcnodata -99.0 -dstnodata -99.0 -co compress=lzw -co BIGTIFF=YES{} {}'.format(datas_str, pathout + '/' + year + '.tif'))
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
    parser.add_argument('-t', '--txt', type=str, help='txt', required=True)# txt路径
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    datas = listdatas(args.input, args.txt)

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for datalist in mpi_data_divide:
        mosaic(datalist, args.output)
    return

if __name__ == '__main__':
    main()

# mpiexec -n 2 python m_.py -i /mnt/e/r_tcc/tcc_new -o /mnt/e/r_tcc/out_1 -t /mnt/e/r_tcc/code/mean.txt -n 2

