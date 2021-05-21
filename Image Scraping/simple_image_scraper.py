#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import re

search_term = input("Enter Search Term: ")
p = re.compile(" ")
search_term = p.sub("%20", search_term)
my_url = "https://www.deviantart.com/search/deviations?q=" + search_term
print(my_url)

r = requests.get(my_url)

soup = BeautifulSoup(r.text, 'html.parser')

count = 1
for img in soup.find_all("img"):
    url = img.get("src")
    if url[:2] == "//":
        url = url[2:]
    #print(url)
    
    os.system("wget -O %d %s" %(count, url))
    file_cmd = "file %d" %(count)
    ext = subprocess.check_output(file_cmd.split()).decode().split()[1].lower()
    os.system("mv %d %d.%s" %(count, count, ext))
    
    count = count + 1
