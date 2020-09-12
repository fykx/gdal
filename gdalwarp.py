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

def warp(data, shp, pathout):
    from osgeo import gdal
    warp_value = 'gdalwarp -cutline {} {} {}'.format(shp, data, pathout + data.split('/')[-1])
    return warp_value

def main():
    pathin = r'E:\YDYL\data\data_98'
    pathout = r'E:\YDYL\data\result_98'
    shp = r'E:\YDYL\bj912\ydyl_912.shp'

    nn = pathout + '/' + 'mybat.bat'
    f = open(nn,'w')

    datas = listdatas(pathin)
    for data in datas:
        warp_value = warp(data, shp, pathout)
        f.write(warp_value)
        f.write('\n')
    f.close()
    return


if __name__ == "__main__":
    main()