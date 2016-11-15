#Easy tool for creating shapefiles with the location information inside images.
#Requires Python Image Library module (https://pypi.python.org/pypi/PIL) and the pyshp module (https://pypi.python.org/pypi/pyshp)

import os
from shapefile import Writer
from PIL import Image
from PIL.ExifTags import TAGS


#adapted from http://stackoverflow.com/questions/765396/exif-manipulation-library-for-python
def get_exif(fn):
    ret = {}
    try:
        i = Image.open(fn)
    
        try:
            info = i._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
            return ret
        except  AttributeError:
            return None
    except IOError:
        return None

folderpath = r'ADD IMAGE FOLDER PATH HERE'
pics = os.listdir(folderpath)
coords = []
for pic in pics:

    # adapted from http://stackoverflow.com/questions/6460381/translate-exif-dms-to-dd-geolocation-with-python
    f = open(os.path.join(folderpath,pic),'rb')
    exif_dic = get_exif(f)
    if exif_dic is not None:
        if 'GPSInfo' in exif_dic.keys():
            lat = [float(x)/float(y) for x, y in exif_dic['GPSInfo'][2]]
            latref = exif_dic['GPSInfo'][1]
            lon = [float(x)/float(y) for x, y in exif_dic['GPSInfo'][4]]
            lonref = exif_dic['GPSInfo'][3]
            f.close()

            lat = lat[0] + lat[1]/60 + lat[2]/3600
            lon = lon[0] + lon[1]/60 + lon[2]/3600
            if latref == 'S':
                lat = -lat
            if lonref == 'W':
                lon = -lon
            vals = lon,lat, pic
            print vals
            coords.append(vals)
        


shpwriter  = Writer(shapeType=1) #Point geometry shapetype
shpwriter.field('Photo') #Attribute field name
for coord in coords:
        print coord
        shpwriter.point(coord[0],coord[1])
        shpwriter.record(coord[2]) #each row consists of a coordinate pair and a record

shpwriter.save(r'ADD OUTPUT FILE PATH HERE')
