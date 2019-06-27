import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re

r = r"(- )+"
data_folder = "../Data/"

def cleaner(text):
  if text:
    if re.findall(r, text):
      return False
    else:
      return True
    
def single_file_creator():
	for season in range(8):
	  url = 'https://genius.com/albums/Game-of-thrones/Season-'+str(season+1)+'-scripts'
	  folder_name =  data_folder + 'season'+str(season+1)
	  os.mkdir(folder_name)
	  
	  response = requests.get(url)
	  soup = BeautifulSoup(response.text, 'html.parser')

	  a = soup.findAll("a", {"class": "u-display_block"})
	  list_links = [data['href'] for data in a]


	  for key, link in enumerate(list_links):
	    url = link
	    response = requests.get(url)
	    soup = BeautifulSoup(response.content, 'html.parser')
	    a = soup.findAll("div", {"class": "lyrics"})
	    data = a[0].text.split('\n')
	    data  = [text for text in data if cleaner(text)]
	    with open(folder_name +"/e"+str(key+1)+".txt", "w") as f:
	      for text in data:
	        f.write(text)
	        f.write("\n")

def file_merger():
	folders = [data_folder+folder_name for folder_name in os.listdir(data_folder)]
	master_list = [folder + '/' + file for folder in sorted(folders) for file in sorted(os.listdir(folder), key=lambda s: int(s[1:-4]))]
	with open(data_folder + 'final_data.txt', 'w') as outfile:
	    for files in master_list:
	        with open(files) as infile:
	            for line in infile:
                        outfile.write(line)

if __name__ == "__main__":
	single_file_creator()
	file_merger()
