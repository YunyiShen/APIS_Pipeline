#This code extract meta-data from camera-trap photos. 
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pytesseract as tes # this is the key package used in this OCR
import os
from pathlib import Path

global Reconyx_entries = {"sequence":(750,0,1000,50),"temp":(1720,0,1920,50), "site":(0,1030,400,1080)} # dangerous global variables, but it can be used globally. Basically the position of the different meta-data

def extract_data(Img_dir,entries_range = Reconyx_entries): # @Img_dir is the path of image, @entries_range is the meta-data want to extract, should be an dictionary, with range of that metadata, see Reconyx_entries for an example
    Img = Image.open(Img_dir) # open the image
    res = {} # result dictionary
    exif_data = Img._getexif()
    
    for entry in list(entries_range.keys()):
        img_temp = Img.crop(entries_range[entry]) # crop out the part of interest
        text = tes.image_to_string(img_temp) # get the meta-data
        res[entry] = text
        
    res["path"] = Img_dir
    res["date_time_exif"] = exif_data[306]
    return(res)


def extract_data_batch(Img_List,entries_range = Reconyx_entries,path = False,save_csv = False, csv_file = None):
    if(path): # if given a folder that contains all the photos
        Img_List = list(Path(".").rglob("*.[jJ][pP][gG] | *.[jJ][pP][eE][gG] | *.[pP][nN][gG]")) # look for all the photos
    
    res = []
    for Img in Img_List:
        res.append(extract_data(Img,entries_range))
        
    if(save_csv): # write csv if needed
        try:
            with open(csv_file, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in res:
                    writer.writerow(data)
        except IOError:
            print("I/O error")
    return(res)


## TODO: Add proof readings 


