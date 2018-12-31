"""
AVA Dataset downloader using ID list.
Put this file and the list file containing (absent) IDs in the same directory.
Usage: python3 ava_downloader_by_ID.py

You can set directory name by changing 'dir_prefix'

Daehyun Bae
Visual Computing Lab at SKKU
2017-09-20

* Image ID 11066 and 397289 are not found
"""
import urllib.request
import requests
import os
import time
import sys
from bs4 import BeautifulSoup

# dpchallenge.com url prefix
URL_prefix = 'http://www.dpchallenge.com/image.php?IMAGE_ID='
dir_prefix = r'absent_Images'
list_file = 'absent_list.csv'
# from dpchallenge robots.txt
delay = 60
split_num = 2000
def download_image(ID):
    try:
        start_time = time.time()
        URL = URL_prefix + ID
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
    except:
        print('Unknown error is occurred skip download this file')

id_list = open(list_file, newline='')

dir_name = dir_prefix
os.makedirs(dir_name, exist_ok=True)
for line in id_list:
    line = line.strip().split(' ')
    imgID = line[0]
    print("Downlaoding " + imgID + ".jpg...")
    download_image(imgID)
    time.sleep(delay)
id_list.close()
print("Download is done.")
