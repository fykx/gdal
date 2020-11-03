def read(shp):
    from osgeo import ogr
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(shp, 0)
    lyr = ds.GetLayer(0)
    extent = lyr.GetExtent()
    return extent

def creatshp(W, E, S, N, pathout, fn):
    from osgeo import ogr, osr

    #创建DataSource，并添加图层
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(4326)

    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(pathout + '/' + fn + '.shp')
    lyr = ds.CreateLayer('extent', sr, ogr.wkbPolygon)

    #添加字段
    fld = ogr.FieldDefn('step', ogr.OFTReal)
    fld.SetWidth(20)
    fld.SetPrecision(2)
    lyr.CreateField(fld)

    start_lat = S
    while start_lat <= N:
        end_lat = start_lat + 0.2

        # 创建几何
        feat = ogr.Feature(lyr.GetLayerDefn())
        ring = ogr.Geometry(ogr.wkbLinearRing)
        ring.AddPoint(W, end_lat)# 左上角
        ring.AddPoint(E, end_lat)# 右上角
        ring.AddPoint(E, start_lat)# 右下角
        ring.AddPoint(W, start_lat)# 右下角
        ring.AddPoint(W, end_lat)# 左上角
        yard = ogr.Geometry(ogr.wkbPolygon)
        yard.AddGeometry(ring)
        feat.SetGeometry(yard)
        # 写入属性
        feat.SetField(0, round(start_lat, 1))
        lyr.CreateFeature(feat)

        start_lat = start_lat + 0.2
    del ds
    return

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-is', '--input_shp', type=str, help='input_shp', required=True)# 输入路径
    parser.add_argument('-o', '--output', type=str, help='output', required=True)# 输出路径
    parser.add_argument('-fn', '--file_name', type=str, help='file_name', required=True)# 输出路径
    args = parser.parse_args()

    W, E, S, N = read(args.input_shp)
    creatshp(W, E, S, N, args.output, args.file_name)
    return

if __name__ == '__main__':
    main()

# python shp.py -is /mnt/e/r_tcc/ne_shp/NE_WGS1984.shp -o /mnt/e/r_tcc/out -fn lat_step
