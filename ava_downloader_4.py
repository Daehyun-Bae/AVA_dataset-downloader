"""
AVA Dataset downloader using ID list.
Put this file and 'AVA.txt' in the same directory.
Usage: python3 ava_downloader_4.py [start_index] [end_index]
Indexes are optional.
Set 'split_num' to divide the number of images each folder. (Default is 2000)
You can set directory name by changing 'dir_prefix'

Daehyun Bae
Visual Computing Lab at SKKU
2017-07-31
"""
import urllib.request
import requests
import os
import time
import sys
from bs4 import BeautifulSoup

# dpchallenge.com url prefix
URL_prefix = 'http://www.dpchallenge.com/image.php?IMAGE_ID='
dir_prefix = r'ava_image'
list_file = 'AVA.txt'
# from dpchallenge robots.txt
delay = 60
split_num = 2000
def download_image(ID):
    start_time = time.time()
    URL = URL_prefix + str(ID)
    # define file name
    file_name = str(ID) + ".jpg"
    full_name = os.path.join(dir_name, file_name)
    source_code = requests.get(URL)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    for img_src in soup.select('#img_container > img'):
        src = img_src.get('src')
        # skip
        if(src == "/images/pix.gif"):
            continue
        # check redundancy
        if os.path.isfile(full_name) == True:
            print(full_name + " is already existed")
            continue
        urllib.request.urlretrieve(src, full_name)
        end_time = time.time()
        print(file_name + " is downloaded at " + dir_name + "\tdownload time: " + str(end_time - start_time))

_start = 0

# check arguments
if len(sys.argv) == 1:
    print("Download whole images in the list.")
    _start = 1
    _stop = -1
elif len(sys.argv) == 2:
    print("You just type the number of images to download. Download is started from first index")
    _start = 1
    if int(sys.argv[1]) <= 0:
        _stop = -1
    else:
        _stop = int(sys.argv[1])
elif len(sys.argv) == 3:
    print("You type the number of images to download. Download is started from first argument")
    _start = int(sys.argv[1])
    if int(sys.argv[2]) <= 0:
        _stop = -1
    else:
        _stop = _start + int(sys.argv[2])
else:
    print("Too many argument input!")
    exit()

id_list = open(list_file)

dir_name = dir_prefix + '1'
os.makedirs(dir_name, exist_ok=True)
for line in id_list:
    line = line.strip().split(' ')
    index = int(line[0])
    imgID = line[1]
    if index < _start:
        index += 1
        continue

    print("Index: " + str(index) + " start: " + str(_start) + " stop: " + str(_stop))
    dir_name = dir_prefix + str(int(index / split_num) + 1)
    if (index % split_num) == 0:
        os.makedirs(dir_name, exist_ok=True)
    download_image(imgID)
    index += 1
    if (_stop > 0) and (index > _stop):
        break
    time.sleep(delay)
id_list.close()
print("Download is done.")
