import os
os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'

def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a


def clip(data, mask, pathout):
    '''影像裁剪'''
    import os
    from osgeo import gdal,ogr,osr

    if os.path.isdir(pathout):
        pass
    else:
        os.makedirs(pathout)

    os.system('gdalwarp -srcnodata 255 -dstnodata 255 -cutline {} {} {}'.format(mask, data, pathout + '/' + 'clip_' + data.split('/')[-1]))
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
    parser.add_argument('-n', '--number', type=int, default=1, help='Number of processes', required=True)# 进程个数
    args = parser.parse_args()

    datas = listdatas(args.input)

    import mpi4py.MPI as MPI
    comm = MPI.COMM_WORLD

    mpi_datas = divide(datas, args.number)
    mpi_data_divide = comm.scatter(mpi_datas, root=0)
    for i in mpi_data_divide:
        clip(i, args.mask, args.output)
    return

if __name__ == '__main__':
    main()
# mpiexec -n 1 python clip.py -i /mnt/e/r_tcc/h1557 -o /mnt/e/r_tcc/out -m /mnt/e/r_tcc/ne_shp/NE_WGS1984.shp -s r_tcc -n 1
# mpiexec -n $NP -hostfile $PBS_NODEFILE python clip.py -i /public/home/mfeng/jwang/forest/northeast/out/loss_gain -o /public/home/mfeng/jwang/forest/northeast/out/loss_gain/clip -m /public/home/mfeng/jwang/forest/northeast/tcc/ne_shp/NE_WGS1984.shp -n $NP


