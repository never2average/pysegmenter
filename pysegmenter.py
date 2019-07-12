from utilities.map import ImageFetcher
from utilities.utils import *
from PIL import Image
import os
import math


def getimage(regionName, bing_api_key,google_api_key,source_option="bing", format = "png", path = None,debug = False):

	if format not in ["jpeg","png"]:
		print("Unknown format provided!! please enter either png or jpeg")
		return
	if source_option not in ["bing","google"]:
		return
	if path is None:
		curr_path = os.getcwd()
		image_path = os.path.join(curr_path, "data", "images")
		if not os.path.isdir(image_path):
			os.makedirs(image_path)
	else:
		if not os.path.isdir(path):
			os.makedirs(path)
		image_path=path
		
	zoom = 17
	width = 2* math.pi * 6378137 / 2 ** (zoom) / 256

	
	reg=Region(regionName)
	

	requiredtiles=[]
	count=1	

	for i in range(-1*reg.radiusx,reg.radiusx):
		for j in range(-1*reg.radiusy,reg.radiusy):
			reg_name="Bengaluru,Karntaka ,India".strip()
			reg_name=[i.lower() if i.isalpha() else " " for i in reg_name]
			reg_name=''.join(reg_name)
			reg_names=reg_name.split()
			reg_first_name=reg_names[0].strip()
			fname=str(reg_first_name)+"_"+str(count)+"."+str(format)
			count+=1
			requiredtiles.append(Tile(reg,i,j,fname))


	for tiles in requiredtiles:
		new_im =  Image.new('RGB', (4096,4096))
		new_im_mask =  Image.new('RGB', (4096,4096))
		for xoffset in range(0,4096,512):
			for yoffset in range(0,4096,512):
				centerWorld = tiles.reg.centerWorld + (Point(tiles.x*4096.0 + xoffset , -1 * (tiles.y * 4096.0 + yoffset)) * width)
				centerGPS = MetersToLonLat(centerWorld)
				imagefetcher=ImageFetcher(
					latitude=centerGPS.y,
					longitude=centerGPS.x,
					length=576,
					imageType="png",
					source="bing" if source_option=="bing" else "googlesat",
					API_Key=bing_api_key if source_option=="bing" else google_api_key,
					debug=debug
				)
				imagefetcher.fetchImage()
				_,im=imagefetcher.cropImage(32)
				new_im.paste(im,(xoffset,yoffset))
				maskfetcher=ImageFetcher(
						latitude=centerGPS.y,
						longitude=centerGPS.x,
						length=576,
						imageType="png",
						source="googleroad",
						API_Key=google_api_key,
						debug=debug
				)
				maskfetcher.fetchImage()
				_,im=maskfetcher.cropImage(32)
				new_im_mask.paste(im,(xoffset,yoffset))
		new_im.save(os.path.join(image_path,tiles.fname))
		new_im_mask.save(os.path.join(image_path,"mask_"+str(tiles.fname)))
