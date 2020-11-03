import os
from osgeo import gdal,ogr,osr

os.environ['PROJ_LIB'] = r'/public/home/mfeng/anaconda3/envs/geo/share/proj'

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, help='input', required=True)# 输入路径
parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
parser.add_argument('-m', '--mask', type=str, help='mask', required=True)# 掩膜
args = parser.parse_args()

os.system('gdalwarp -dstnodata -99.0 -cutline {} {} {}'.format(args.mask, args.input, args.output))

# python clip_1.py -i /public/home/mfeng/jwang/forest/northeast/dem/Reproject/reproj.tif -o /public/home/mfeng/jwang/forest/northeast/dem/Reproject/clip_dem.tif -m /public/home/mfeng/jwang/forest/northeast/tcc/ne_shp/NE_WGS1984.shp