#This code extract meta-data from camera-trap photos. 
from PIL import Image
import pytesseract as tes
import os
from pathlib import Path

global Reconyx_entries = {"date_time":(0,0,750,50),"type":(750,0,1000,50),"temp":(1720,0,1920,50), "site":(0,1030,400,1080)} # dangerous thing, but it can beused globally

def extract_data(Img_dir,entries_range = Reconyx_entries): # image is the image, entries should be the meta-data want to extract, should be an dictionary, with range of that metadata
    Img = Image.open(Img_dir)
    res = {}
    
    for entry in list(entries_range.keys()):
        img_temp = Img.crop(entries_range[entry])
        text = tes.image_to_string(img_temp)
        if entry=="date_time":
            text = text.replace(";",":")
            text = text.replace("O","0") # several simple proof reading
        res[entry] = text
        
    res["path"] = Img_dir
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


## TODO: Add proof reading  

