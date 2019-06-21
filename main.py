from utilities.bing import ImageFetcher
from utilities.utils import *
import os
import re


def getimage(regionname, format, api_key, path=r"./data/images"):
	if format not in ["jpeg","png"]:
		print("Unknown format provided!! please enter either png or jpeg")
		return
		
	if not os.path.isdir(path):
		os.mkdir(path)
		
	zoom = 17
	width = 2* math.pi * 6378137 / 2 ** (zoom) / 256

	reg=region(regionname)

	requiredtiles=[]
	count=1	

	for i in range(-1*reg.radiusx,reg.radiusx):
		for j in range(-1*reg.radiusy,reg.radiusy):
			reg_name=reg.name.strip()
			reg_names=re.split(', |; |  |. |: ')
			reg_first_name=reg_names[0].strip()
			fname=str(reg_first_name)+"_"+str(count)+"."+str(format)
			count+=1
			requiredtiles.append(tile(reg,i,j,fname))
			

	for tiles in requiredtiles:
		new_im = Image.new('RGB', (4096,4096))
		for xoffset in range(0,4096,512):
			for yoffset in range(0,4096,512):
				centerWorld = tiles.reg.centerWorld + (Point(tiles.x*4096.0 + xoffset , -1 * (tiles.y * 4096.0 + yoffset)) * width)
				centerGPS = MetersToLonLat(centerWorld)
				imagefetcher=ImageFetcher(
					point=centerGPS,
					length=576,
					imageType=format,
					source="bing",
					API_Key=api_key)
				imagefetcher.fetchImage()
				_, im = imagefetcher.cropImage(32)
				new_im.paste(im, (xoffset, yoffset))
		new_im.save(path+"/"+str(tiles.fname))