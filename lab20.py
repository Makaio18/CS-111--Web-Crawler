# *WRITE YOUR CODE IN THIS FILE

import urllib.parse
import requests

"""
Segement validates url uages and reallness in accessing data from the website. 
Validates the user inputed url by comparing its stucture to the uniformed method in which URLS should be represented. 
Futhermore, code segement, fixes any unfinshed, or "broken" urls that are inputed, are used for the conitunation of the crawling. 
"""


"""
______Libs________
  urllib.parse: Allows for the breaking down of url into(sheme, net-loc, and path.)
  requests: Allows for higher level Interactions of url( handle web data more easily)

______Methods______
  get_domain()------ 
  combine_paths()---
  combine_urls()---
  print_pages()---
"""


#returns the domain of the current url link
def get_domain(url):

 URL = urllib.parse.urlparse(url)
 
 if (URL.scheme in ("http", "https")):
    return URL.scheme + "://" + URL.netloc
 else:

    # will reuturn empyty sting if nothing is present, this allows 
    # for future comparsions to adjust in sqequecing, if this case not met
    return ""

# Takes, current domain, and creates link with desired path. 
#  ( creating a valid link with agreed upon domian, but differing paths)
def combine_paths(url, path):
  URL = urllib.parse.urljoin(url, path) 
  return  URL


# just combines urls in general----- scnenario basesd, if a url is just missing the domain( 
# this method will appl remaing path )
def combine_urls(base, second):
  URL = urllib.parse.urljoin(base, second) 
  return URL


      

           

    





  
