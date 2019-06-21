import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x)+","+str(self.y)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __mul__(self, scale):
        return Point(self.x * scale, self.y * scale)
		
		
class region:
    def __init__(self, name):
        self.name = name
        self.get_bbox()
        self.get_center_gps()
        self.get_radii()        
        
    def get_bbox(self):
        testobj=GeoEncoder()
        self.bbox=testobj.fetchBoundingBox(self.name)
    
    def get_center_gps(self):
        center_x = (self.bbox[1] + self.bbox[3]) / 2.0
        center_y = (self.bbox[0] + self.bbox[2]) / 2.0
        self.centerGPS = Point(center_x, center_y)
        self.centerWorld = LonLatToMeters(self.centerGPS)
        
    def get_radii(self):
        extreme = LonLatToPixel(Point(self.bbox[1], self.bbox[0]), self.centerGPS, zoom)
        self.radiusx = int(math.ceil(abs(extreme.x) / 4096))
        self.radiusy = int(math.ceil(abs(extreme.y) / 4096))

		
class tile:    
    def __init__(self, region, x, y, fname):
        self.reg = region
        self.x = x
        self.y = y
        self.fname = fname
        
    def __str__(self):
        return self.reg.name+" "+str(self.x)+" "+str(self.y)+" "+self.fname
		

def LonLatToMeters(lonlat_point):
    origin_shift = 2 * math.pi * 6378137 / 2.0
    metre_x = lonlat_point.x * origin_shift / 180.0
    metre_y = math.log(math.tan((90 + lonlat_point.y) * math.pi / 360.0))
    metre_y /= (math.pi / 180.0)
    metre_y = metre_y * origin_shift / 180.0
    return Point(metre_x, metre_y)


def MetersToLonLat(meter_point):
    origin_shift = 2 * math.pi * 6378137 / 2.0
    lonlat_x = (meter_point.x / origin_shift) * 180.0
    lonlat_y = (meter_point.y / origin_shift) * 180.0
    lonlat_y = 180 / math.pi * (2 * math.atan(math.exp(lonlat_y * math.pi / 180.0)) - math.pi / 2.0)
    return Point(lonlat_x, lonlat_y)


def GetMetersPerPixel(zoom):
    return 2 * math.pi * 6378137 / 2**(zoom*1.0) / 256


def LonLatToPixel(p, origin, zoom):
    p = LonLatToMeters(p)-LonLatToMeters(origin)
    p = p * (1 / GetMetersPerPixel(zoom))
    p = Point(p.x, -p.y)
    p = p + Point(256, 256)
    return p


def PixelToLonLat(p, origin, zoom):
    p = p - Point(256, 256)
    p = Point(p.x, -p.y)
    p = p * GetMetersPerPixel(zoom)
    p = MetersToLonLat(p + LonLatToMeters(origin))
    return p


def LonLatToMapboxTile(lonLat, zoom):
    n = 2**(zoom*1.0)
    xtile = int((lonLat.x + 180) / 360 * n)
    ytile = int((1 - math.log(math.tan(lonLat.y * math.pi / 180) + (1 / math.cos(lonLat.y * math.pi / 180))) / math.pi) / 2 * n)
    return (xtile, ytile)


def LonLatToMapbox(lonLat, zoom, originTile):
    n = 2**(zoom*1.0)
    x = (lonLat.x + 180) / 360 * n
    y = (1 - math.log(math.tan(lonLat.y * math.pi / 180) + (1 / math.cos(lonLat.y * math.pi / 180))) / math.pi) / 2 * n
    xoff = x - originTile[0]*1.0
    yoff = y - originTile[1]*1.0
    return Point(xoff, yoff)*256


def MapboxToLonLat(p, zoom, originTile):
    n = 2**(zoom*1.0)
    p = (p * (1.0/256)) + (Point((originTile[0]*1.0), (originTile[1]*1.0)))
    x = p.x * 360 / n - 180
    y = math.atan(math.sinh(math.pi * (1 - 2 * p.y / n)))
    y = y * 180 / math.pi
    return Point(x, y)
