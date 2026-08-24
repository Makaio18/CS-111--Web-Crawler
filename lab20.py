# *WRITE YOUR CODE IN THIS FILE

import urllib.parse
import requests


def get_domain(url):

 URL = urllib.parse.urlparse(url)
 
 if URL.scheme == "http" or URL.scheme == "https":
    return URL.scheme + "://" + URL.netloc
 
 else:
    return ""

def combine_paths(url, path):
  URL = urllib.parse.urljoin(url, path) 
  return  URL


def combine_urls(base, second):
  URL = urllib.parse.urljoin(base, second) 
  return URL


def print_pages(url, plist, output_file):
  URL = ""
  with open(output_file, 'w') as filename:

    for paths in plist:
        if paths.startswith("/"):

            URL =  urllib.parse.urljoin(url, paths) 
        else:
            URL =  urllib.parse.urljoin(URL, paths) 
           
        content = requests.get(URL)
        filename.write(content.text)
        filename.write("\n")




      

           

    





  
