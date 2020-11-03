from osgeo import gdal
from osgeo import gdalconst
import os

# 打开tif文件
ref_ds = gdal.Open("/public/home/mfeng/jwang/forest/northeast/out/mean/2/mean_mosaic.tif", gdalconst.GA_ReadOnly) # 参考文件
in_ds  = gdal.Open("/public/home/mfeng/jwang/forest/northeast/dem/Reproject/clip_dem.tif",gdalconst.GA_ReadOnly) # 输入文件

# 参考文件与输入文件的的地理仿射变换参数与投影信息
in_trans = in_ds.GetGeoTransform()
in_proj = in_ds.GetProjection()
ref_trans = ref_ds.GetGeoTransform()
ref_proj = ref_ds.GetProjection()

print(in_trans, ref_trans)

