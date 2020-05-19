'''
File: Resample.py
Author: 王建邦
Version: 0.1
Create: 2019-08-02
Description: 栅格数据逐像元非线性拟合，并在对应区间积分后输出栅格
'''

import os
import gdal
import numpy as np
from scipy.optimize import curve_fit
import pylab as pl
from osgeo import gdal
import matplotlib.pyplot as plt
from scipy.integrate import tplquad,dblquad,quad

'''列出数据'''
def listdatas(pathin):
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i[-4:] == '.tif':
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

'''定义拟合函数'''
def func(x, a, b, c):
    return a * x ** 2 + b * x + c

def main(pathin, pathout):
    a = listdatas(pathin)#栅格数据列表
    b = []#数据数组列表
    
    #遍历数据，将tif存为数组
    for band_fn in a:
        in_ds = gdal.Open(band_fn)
        in_band = in_ds.GetRasterBand(1)#波段索引从1开始
        in_data = in_band.ReadAsArray()
        b.append(in_data)
        xsize = in_band.XSize#列
        ysize = in_band.YSize#行

    #构建输出数组
    out_data = np.zeros(shape=(ysize, xsize))

    #新建数据集
    gtiff_driver = gdal.GetDriverByName('GTiff')
    out_ds = gtiff_driver.Create(pathout + '/' + 'new.tif', xsize, ysize, 1, in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
        
    #数据读取
    for x in range(xsize):#遍历列
        for y in range(ysize):#遍历行
            data_list = []
            for arr in b:#遍历数组
                nodata = in_band.GetNoDataValue()
                data_list.append(arr[y, x])
            if nodata in data_list or sum(data_list) == 0 or -0.5 in data_list or -1 in data_list:#判断无效值
                out_data[y, x] = nodata#写入nodata
            else:
                #移除列表前方的0
                i_f = len(data_list)
                j_f = 0
                while j_f <= i_f:
                    if data_list[0] == 0.0 and data_list[1] == 0.0:
                        data_list.remove(data_list[0])
                    j_f = j_f + 1
                data_list.remove(data_list[0])

                #移除列表后方的0
                i_a = len(data_list)
                j_a = 0
                while j_a <= i_a:
                    if data_list[-1] == 0.0 and data_list[-2] == 0.0:
                        data_list.remove(data_list[-1])
                    j_a = j_a + 1
                data_list.remove(data_list[-1])

                #数据拟合
                data_list_arr = np.array(data_list)#data数组
                time_list_arr = np.array(range(len(data_list)))#时间序列数组
                popt, pcov = curve_fit(func, time_list_arr, data_list_arr)
                func_a = popt[0]
                func_b = popt[1]
                func_c = popt[2]

                
                #拟合绘图(谨慎使用，占用大量运行内存)
                fig,ax = plt.subplots(1,1,figsize=(6,4))
                plt.plot(time_list_arr, data_list_arr, ls = "-", lw = 2,label = "data")
                plt.plot(time_list_arr, func(time_list_arr, func_a, func_b, func_c), ls = "-", lw = 2,label = "nh")
                plt.legend()
                #plt.show()#危险语句挑战运行内存
                fig.savefig(pathout + '/' + str(y) + '_' + str(x) + '.png', dpi=300, bbox_inches='tight')#危险语句挑战运行内存
                
                
                #积分
                val1, err1 = quad(lambda x: func_a * x ** 2 + func_b * x + func_c, time_list_arr[0] - 1, time_list_arr[-1] + 1)
                out_data[y, x] = round(val1, 2)#写入积分值（保留两位小数）
                
    #数据输出            
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(out_data)
    out_band.SetNoDataValue(nodata)#设置nodata
    out_band.FlushCache()
    out_band.ComputeStatistics(False)              
    return

                               
if __name__ == "__main__":
    pathin = r'C:\Users\fykx\Desktop\11\test\02clip'
    pathout = r'C:\Users\fykx\Desktop\11\test\out'
    main(pathin, pathout)
    
    
