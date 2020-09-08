'''
Descripttion: 镶嵌栅格
version: 0.1
Author: Jianbang Wang
Date: 2020-08-27 19:30:20
'''
def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def mosaic(datas, pathout):
    from osgeo import gdal

    nn = pathout + '/' + 'mysh.sh'
    f = open(nn,'w')

    f.write('gdal_merge.py -o {} -a_nodata -99.0 '.format(pathout + '/' + 'DB_mean' + '.tif'))
    for i in datas:
        f.write('{} '.format(i))
    f.close()
    return

def main():
    pathin = r'/home/forest/NEChina/out/mean/1'
    pathout = r'/home/forest/NEChina/out/mean/2'
    datas = listdatas(pathin)
    mosaic(datas, pathout)
    return


if __name__ == "__main__":
    main()