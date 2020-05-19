'''
File: Proportion of nodata.py
Author: 王建邦
Version: 0.1
Create: 2019-08-08
Description: 查看栅格NoData比例
'''

'''列出数据'''
def listdatas(pathin):
    import os
    _a = []
    _datas = os.listdir(pathin)
    for _i in _datas:
        if _i[-4:] == '.tif':
            _fn_i = pathin + '/' + _i
            _a.append(_fn_i)
    return _a

def main(pathin, pathout):
    import numpy as np
    from osgeo import gdal
    
    #新建txt
    _nn = pathout + '/' + 'Statistics.txt'
    _f = open(_nn, 'w')
    
    _a = listdatas(pathin)#栅格数据列表

    _b = []

    for _fn in _a:
        _in_ds = gdal.Open(_fn)
        _in_band = _in_ds.GetRasterBand(1)#波段索引从1开始
        _in_arr = _in_band.ReadAsArray()
        
        _in_arr.shape = 1, -1
        
        _xsize = _in_band.XSize#列
        _ysize = _in_band.YSize#行

        _nodata = str(_in_band.GetNoDataValue())
        
        _Percentage = str(_in_arr.tolist()).count(_nodata)/(_xsize * _ysize)
        
        _f.write("{},{:.4f}\n".format(_fn.split('/')[-1].split('.')[0], _Percentage))
        _b.append(_Percentage)
        print(_fn.split('/')[-1].split('.')[0], "  ", round(_Percentage, 4))
        
    _f.write("{},{:.4f}\n".format('mean', sum(_b)/len(_b)))
    _f.close()
    return
                         
if __name__ == "__main__":
    pathin = r'F:\data_fykx\High Mountain Asia 8-meter DEMs Derived from Along-track Optical Imagery'
    pathout = r'F:\data_fykx\High Mountain Asia 8-meter DEMs Derived from Along-track Optical Imagery\metadata'
    main(pathin, pathout)
    
