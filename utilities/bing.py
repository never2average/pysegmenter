import requests
import shutil
import os
from PIL import Image

baseURLs = {
    "bing": "https://dev.virtualearth.net/REST/V1/Imagery/Map/Aerial/{}%2C{}/{}?mapSize={},{}&format={}&key={}"
}


class ImageFetcher:
    def __init__(self, *args, **kwargs):
        self.zoom = 17
        self.fetchedImage = False
        self.fileSaved = False
        self. validationError = self._validate_inputs(**kwargs)

    def _validate_inputs(self, **kwargs):
        if len(kwargs.keys()) == 6 or len(kwargs.keys()) == 7:
            if "latitude" in kwargs:
                self.latitude = kwargs["latitude"]
            else:
                print("Key Error: The arguement latitude is a required value")
                return True

            if "longitude" in kwargs:
                self.longitude = kwargs["longitude"]
            else:
                print("Key Error: The arguement longitude is a required value")
                return True

            if "length" in kwargs:
                self.length = kwargs["length"]
            else:
                print("Key Error: The arguement length is a required value")
                return True

            if "breadth" in kwargs:
                self.breadth = kwargs["breadth"]
            else:
                self.breadth = self.length

            if "source" in kwargs:
                self.source = kwargs["source"]
                if not kwargs["source"] in baseURLs:
                    print(
                        "Source Error: Unknown source {}.".format(
                            kwargs["source"]
                        )
                    )
                    print(
                        "Available Options are: {}.".format(
                            ','.join(baseURLs.keys())
                        )
                    )
                    return True
                else:
                    self.sourceStr = baseURLs[kwargs["source"]]
            else:
                print("Key Error: The arguement source is a required value")
                return True

            if "API_Key" in kwargs:
                self.apikey = kwargs["API_Key"]
            else:
                print("Key Error: The arguement API Key is a required value")
                return True

            if "imageType" in kwargs:
                self.imageType = kwargs["imageType"]
            else:
                print("Key Error: The arguement imageType is a required value")
                return True
            return False
        else:
            print(
                "Variable Error: The class requires 6 arguements."
            )
            print(
                "You gave {} arguements".format(len(kwargs.keys()))
            )
            return False

    def fetchImage(self):
        if not self.validationError:
            return self._fetchImage()

    def _fetchImage(self):
        if self.source == "bing":
            self.image = requests.get(
                self.sourceStr.format(
                    self.latitude, self.longitude, self.zoom, self.length,
                    self.breadth, self.imageType, self.apikey
                ),
                stream=True
            )
            if self.image.status_code == 200:
                self.image.raw.decode_content = True
                self.fetchedImage = True
                print("Image Fetched Successfully")
            else:
                print("Image Fetching Failed")
            return self.image.status_code

    def saveImage(self, dir, filename):
        if not self.validationError:
            return self._saveImage(dir, filename)

    def _saveImage(self, dir, filename):
        if not os.path.isdir(dir):
            try:
                os.makedirs(dir)
            except Exception:
                print("Failed to make directory.")
                print("Make sure you have appropriate user privileges.")
                return "Error"
        try:
            self.fileAddress = dir+"/"+filename+"."+self.imageType
            with open(self.fileAddress, 'wb') as fobj:
                shutil.copyfileobj(self.image.raw, fobj)
            self.fileSaved = True
            print("Image Saved Sucessfully")
            return "Success"
        except Exception:
            print("Error Occured While Saving Image")
            return "Error"

    def cropImage(self, pixels):
        if self.fetchedImage and self.fileSaved:
            return self._cropImage(pixels)

    def _cropImage(self, pixels, **kwargs):
        try:
            if self._checkPathValidity(**kwargs):
                image = Image.open(self.image.raw)
                imageWidth, imageHeight = image.size
                image.crop(
                    (pixels, pixels, imageWidth-pixels, imageHeight-pixels)
                )
                print("Image Cropped Successfully to size {}X{}.".format(
                    imageHeight-2*pixels, imageWidth-2*pixels
                ))
                return "CropSuccess", image
            else:
                print("An error occured while cropping the Image.")
                return "CropError", Image.new("RGB",(512,512))
        except Exception:
            print("An error occured while cropping the Image.")
            return "CropError", Image.new("RGB",(512,512))

    def _checkPathValidity(self, **kwargs):
        if kwargs == {}:
            return True
        else:
            if "dir" in kwargs:
                if not os.path.isdir(kwargs["dir"]):
                    print("The directory provided by you does not exist.")
                    return False
                else:
                    if "filename" in kwargs:
                        self.fileAddress += kwargs["dir"]
                        self.fileAddress += "/"+kwargs["filename"]
                        self.fileAddress += "."+self.imageType
                        return True
                    else:
                        print("filename is a required attribute.")
                        return False
            else:
                print("dir is a required attribute.")
