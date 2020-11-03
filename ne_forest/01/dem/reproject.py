from osgeo import gdal
from osgeo import gdalconst
import os

# 打开tif文件
ref_ds = gdal.Open("/public/home/mfeng/jwang/forest/northeast/out/mean/2/mean_mosaic.tif", gdalconst.GA_ReadOnly) # 参考文件
in_ds  = gdal.Open("/public/home/mfeng/jwang/forest/northeast/dem/mosaic/dem_mosaic.tif",gdalconst.GA_ReadOnly) # 输入文件

# 参考文件与输入文件的的地理仿射变换参数与投影信息
in_trans = in_ds.GetGeoTransform()
in_proj = in_ds.GetProjection()
ref_trans = ref_ds.GetGeoTransform()
ref_proj = ref_ds.GetProjection()

# 参考文件的波段参考信息
band_ref = ref_ds.GetRasterBand(1)
# 参考文件行列数
x = ref_ds.RasterXSize 
y = ref_ds.RasterYSize

# 创建输出文件
driver= gdal.GetDriverByName('GTiff')
output = driver.Create('/public/home/mfeng/jwang/forest/northeast/dem/Reproject/reproj_1.tif', x, y, 1, band_ref.DataType)
# 设置输出文件地理仿射变换参数与投影
output.SetGeoTransform(ref_trans)
output.SetProjection(ref_proj)

# 重投影，插值方法为双线性内插法
gdal.ReprojectImage(in_ds, output, in_proj, ref_proj, gdalconst.GRA_NearestNeighbour)

# 关闭数据集与driver
in_ds1 = None
in_ds2 = None
drive  = None
output = None

