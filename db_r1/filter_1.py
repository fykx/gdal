def listdatas(pathin):
    import os
    a = []
    datas = os.listdir(pathin)
    for i in datas:
        if i.endswith('.tif'):
            fn_i = pathin + '/' + i
            a.append(fn_i)
    return a

def filter(shp_point, mask, path):
    from osgeo import ogr,gdal

    ds_point = ogr.Open(shp_point,1)
    lyr_point = ds_point.GetLayer(0)

    lyr_point.SetSpatialFilter(mask)

    
    #key_head = [q*1 for q in range(len(head))]
    #dict_head = dict(zip(key_head,head))

    datas = []
    if lyr_point.GetFeatureCount() != 0:
        for feat in lyr_point:
            feat_data = []
            geometry = feat.GetGeometryRef()
            x = geometry.GetX()
            y = geometry.GetY()

            tifs = listdatas(path)
            value_dic = {}
            for tif in tifs:
                key_list = tif.split('/')[-1].split('_')[1:4]
                key = key_list[0] + '_' + key_list[1] + '_' + key_list[2]
                in_ds = gdal.Open(tif)
                in_band = in_ds.GetRasterBand(1)#波段索引从1开始
                in_data = in_band.ReadAsArray()

                transform = in_ds.GetGeoTransform()
                xOrigin = transform[0]#左上角位置
                yOrigin = transform[3]#左上角位置
                pixelWidth = transform[1]#像元宽度
                pixelHeight = transform[5]#像元高度

                xOffset = int((x-xOrigin)/pixelWidth)
                yOffset = int((y-yOrigin)/pixelHeight)
                
                value = in_data[yOffset,xOffset]
                value_dic[key] = value
            feat_data.append(x)
            feat_data.append(y)
            feat_data.append(value_dic)
            datas.append(feat_data)
    return datas

def main():
    from osgeo import ogr,gdal
    mask_data = r'/mnt/e/r1/out/union/proj_out.shp'
    shp_point = r'/mnt/e/r1/point/db.shp'
    pathout = r'/mnt/e/r1/out/csv'

    nn = pathout + '/' + 'result_1.csv'
    f = open(nn, 'w')
    
    head = ['x','y','loss_year_n0','loss_year_n1','loss_year_n2','loss_prob_n0','loss_prob_n1','loss_prob_n2','gain_year_n0','gain_year_n1','gain_year_n2','gain_prob_n0','gain_prob_n1','gain_prob_n2']
    for h in range(len(head)):
        f.write('{},'.format(head[h]))
    f.write('\n')

    ds = ogr.Open(mask_data, 0)
    lyr = ds.GetLayer(0)
    
    set_datas = []
    xys = []
    for feat in lyr:
        mask = feat.geometry().Clone()
        value = feat.GetField('name')
        path = value.replace('/' + value.split('/')[-1], '')
        datas = filter(shp_point, mask, path)
        if len(datas) != 0:
            for data in datas:
                if data in set_datas:
                    pass
                else:
                    set_datas.append(data)
                    xys.append(str(data[0]) + '_' + str(data[1]))
    set_xys = list(set(xys))
    for xy in set_xys:
        xys.remove(xy)

    for feat_data in set_datas:
        if str(feat_data[0]) + '_' + str(feat_data[1]) in xys:
            pass
        else:
            f.write('{},{},'.format(feat_data[0],feat_data[1]))
            value_dic = feat_data[2]
            for i in range(len(value_dic)):
                f.write('{},'.format(value_dic[head[i+2]]))
            f.write('\n')
    f.close()
    return


if __name__ == "__main__":
    main()