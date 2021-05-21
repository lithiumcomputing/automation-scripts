#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import re
from threading import Thread, Lock

count = 1

MAX_THREADS = 8
num_of_threads = 0
lock = Lock()

def download(count, url):
    global num_of_threads

    os.system("wget -qO %d \"%s\"" %(count, url))
    file_cmd = "file %d" %(count)
    ext = subprocess.check_output(file_cmd.split()).decode().split()[1].lower()
    os.system("mv %d %d.%s" %(count, count, ext))

    lock.acquire()
    num_of_threads -= 1
    lock.release()
    
def recursive_search(my_url, level=2):
    global count
    global lock
    global num_of_threads

    if level == 0:
        return
    r = requests.get(my_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    imgs = soup.find_all("img")
    widths=[]
    p_art = re.compile("https://www.deviantart.com/[A-Za-z0-9\-]*/art/.*")
    if p_art.match(my_url) != None:  
        for img in imgs:
            url = img.get("src")
              
            style = img.get("style")
            if style != None:
                style=style.strip()
                style_list = style.split(";")
                has_width = False
                for item in style_list:
                    if "width" in item and re.compile("^http").match(url.strip()):
                        widths.append(float(re.compile("[A-za-z\:]*").sub("", item)))
                        has_width = True
                        break
                if not has_width:
                    widths.append(0)
            else:
                widths.append(0)
                
        if len(widths) > 0:
            idx_maxwidth = widths.index(max(widths))
            url = imgs[idx_maxwidth].get("src")
            print("DOWNLOAD: {}".format(url))
            can_run = False
            while not can_run:
                lock.acquire()
                can_run = num_of_threads < MAX_THREADS
                lock.release()
            
            lock.acquire()
            num_of_threads += 1
            lock.release()
            Thread(target=download, args=(count, url)).start()
                
            count += 1
        
    for element in soup.find_all(attrs={"data-hook": "deviation_link"}):
        url = element.get("href")
        if url[:2] == "//":
            url = url[2:]
        print("URL: {}\nFound at LVL: {}".format(url, level))
        recursive_search(url, level-1)

search_term = input("Enter search term: ").strip()
p = re.compile(" ")
search_term = p.sub("%20", search_term)
my_url = "https://www.deviantart.com/search/deviations?q=" + search_term

recursive_search(my_url, level=3)
