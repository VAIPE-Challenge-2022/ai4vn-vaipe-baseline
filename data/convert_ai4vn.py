import json
import os
import os.path as osp
from PIL import Image, ExifTags
from tqdm import tqdm
import shutil

for orientation in ExifTags.TAGS.keys():
    if ExifTags.TAGS[orientation] == 'Orientation':
        break

def exif_size(img):
    # Returns exif-corrected PIL size
    s = img.size  # (width, height)
    try:
        rotation = dict(img._getexif().items())[orientation]
        if rotation == 6:  # rotation 270
            s = (s[1], s[0])
        elif rotation == 8:  # rotation 90
            s = (s[1], s[0])
    except:
        pass

    return s

dataset_path = "data/ai4vn"
if not osp.exists(dataset_path):
    os.makedirs(dataset_path)
    os.makedirs(osp.join(dataset_path, "images"))
    for s in ["train", "val"]:
        os.makedirs(osp.join(dataset_path, "images", s))
        os.makedirs(osp.join(dataset_path, "labels", s))
for set_data in ["public_train", "public_test"]:
    if set_data == "public_train":
        s = "train"
    elif set_data == "public_test":
        s = "val"
    path = "/home/ubuntu/shared/{}/pill/".format(set_data)
    for file in tqdm(os.listdir(osp.join(path, "label"))):
        if file.endswith(".json"):
            with open(osp.join(path, "label", file)) as f:
                data = json.load(f)
                image_path = osp.join(path, "image", file.replace(".json", ".jpg"))
                img = Image.open(image_path)
                shutil.copy(image_path, osp.join(dataset_path, "images", s, file.replace(".json", ".jpg")))
                w,h = exif_size(img)
                for box in data:
                    label = box['label']
                    x_mid = (box["x"]/w + box["x"]/w + box["w"]/w)/2
                    y_mid = (box["y"]/h + box["y"]/h + box["h"]/h)/2
                    w_norm = box["w"]/w
                    h_norm = box["h"]/h
                    with open(osp.join(dataset_path, "labels", s ,file.replace(".json", ".txt")), 'a') as f:
                        f.write(f'{label} {x_mid} {y_mid} {w_norm} {h_norm}\n')
        else:
            print("no json")
            break