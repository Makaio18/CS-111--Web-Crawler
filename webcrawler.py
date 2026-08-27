import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import lab20 as combineLinks
import image_processing
import RequestGuard
import requests
import sys
import csv


"""
======LIBS=================
    matplotlib
    beautifulsoup
    requests
    sys
    csv

=====Modules======
    lab20
    image_processing
    RequestGuard

====Functions===============
    modify()
    plot_data()
    fix_links()
    count_links()
    main()
    test_flags()


===========SAMPLE INIPUT
# -p http://cs111.byu.edu/Projects/project04/assets/data.html data.png data.csv
# -i http://cs111.byu.edu/Projects/project04/assets/images.html grey_ -g
# -c <url> <output filename 1> <output filename 2>
"""

# ________________
def modify_img(url, file_name, flag):

    #calls the  contents of the URL saves it as a response object.
    response = requests.get(url)

    #Beautiful soup, pulls data out of html, using preferred parser( by creating its own cutsom tree object) mimics dom object
    #stores tree object( Herirchal relationship)
    soup = BeautifulSoup(response.text, features="html.parser")

    #empty list, that will store all future images of a particular 
    imgLst = []


    #method that finds that locates all img nodes within the tree brancg and, then identifies, whether if the resource for the imge is 
    #interanlly stored or externally, if stored locally, then retirive img, create a full URL of the img refrence, and then add 
    #completed url to list of imgs. 
    #SRC is to download,
    #href acts like a pointer. 
    for img in soup.find_all("img"):
        #finds the embeded and downloaded reosurces, ones that are not pointed in another direction.
        src = img.get("src")
        if src:
            content = fix_links(src, url)
            imgLst.append(content)

    
    """
    loops over all img in list, splits off params, 
    creates a new varible name---- which is a string containing a file-path
    
    """
    for imgUrl in imgLst:
        #splits imge url parts up. 
        split = imgUrl.split("/")

        #Takes website, and adds the final parameter of the image url, 
        # stores, name of affect, last segment in full url as shorten file_name
        name = file_name + split[len(split) - 1]

        #calls the image resource it self, using full url then stores it to the repsonse object
        response = requests.get(imgUrl)

        #opens a new file, where the name of file is "name" and the contents are the acutual contents saved from the 
        #response object contents()
        # the request can only call, saving it to a varible that has arrtibutes regarding not the address rather the data itself
        #allows us to write saved data to new file. 
        with open(name, 'wb') as imgUrl:
            imgUrl.write(response.content)



        #using new resource saved, we apply the filter using imported module, and adjust sequencing using flag. 
        image_processing.apply_filter(name, flag)
        

    

def plot_data(url, plot_png, output_file):

    response = requests.get(url)
    if (response.status_code != 200) :
        print("Page doesn't exist")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', id='CS111-Project4b')
    if not table:
        return

    x_values = []
    y_values = []

    for row in table.find_all('tr') :
        cells = row.find_all('td')
        if (len(cells) < 1) :
            continue
        
        try:
            x = float(cells[0].text)
            x_values.append(x)

            
            if (not y_values) :
                y_values = [[] for _ in range(len(cells) - 1)]

            for i in range(1, len(cells)) :
                y = float(cells[i].text)
                y_values[i-1].append(y)


        except ValueError:
            print("Could not convert data to float, skipping row.")
            continue

   
    colors = ['blue', 'green', 'red', 'black']


    for i, y in enumerate(y_values):
        plt.plot(x_values, y, color=colors[i % len(colors)], label=f'Dataset {i+1}')

    plt.savefig(plot_png)
    plt.close()


    
    with open(output_file, 'w', newline='') as out_put_file:
        writer = csv.writer(out_put_file)
        for row in zip(x_values, *y_values):
            writer.writerow(row)

    


def fix_links(current_href, parentDomain):

    domain = combineLinks.get_domain(parentDomain)

    if (current_href.startswith("https") or current_href.startswith("http")) :  

        if ("#" in current_href) :
            return current_href.split("#")[0] 
        else:
            return current_href 


    
    elif (current_href.startswith("/")) :  
        return combineLinks.combine_paths(domain, current_href) 



    elif (current_href.startswith("#")) : 
        return parentDomain



    else: 
        return combineLinks.combine_urls(parentDomain, current_href) 
        


#_______________________-Counting the links on the page_______
"""
Abiding by the 

"""
def count_links(inputURL, output1, output2):

    linkstoVist = []
    timesAppeared = {}
    guard = RequestGuard.RequestGuard(inputURL)
    linkstoVist.append(inputURL)

    
    while linkstoVist:
        
        currentLink = linkstoVist.pop()

        if (currentLink in timesAppeared) : ### check if I've visited link
            timesAppeared[currentLink] += 1
            continue
        
        timesAppeared[currentLink] = 1

        if (guard.can_follow_link(currentLink)) :
            print(currentLink)

            response = requests.get(currentLink)
            soup = BeautifulSoup(response.text, "html.parser")
            
            for tag in soup.find_all("a"): #### FIRST LAYER OF LINK gets all tags on page

                href = tag.get("href") ### The links on a page
                fixedLink = fix_links(href, currentLink ) ### Fixes the url if not complete

                print(fixedLink)
                linkstoVist.append(fixedLink)

                print(f"Orginal Link: {href}\n Fixed link: {fixedLink}\n")

    print(timesAppeared)

    BINSIZE = []
    VAlUES = timesAppeared.values()
    max_range = max(timesAppeared.values()) + 1
    

    for i in range(1, max_range + 1):
        BINSIZE.append(i)

    NEWVALUES, NEWBINS, temp = plt.hist(VAlUES,BINSIZE)
    plt.savefig(output1)
    plt.close()

    with open(output2, "w") as output_file2:
        for i in range(len(NEWVALUES)):
            output_file2.write(f"{NEWBINS[i]},{NEWVALUES[i]}\n")



#_______saves sys args and flags to vars, 
def main(argv):

    # action (which function) being performed
    flag = argv[1]
    #where the action will be preformed


    url = argv[2]
    #Resource one (etc. img, data, infomation)
    elem1 = argv[3]
    #Resource two (either more data, img,) or futher detail pretain to action being done on resource one
    elem2 = argv[4]

    # -c <url> <output filename 1> <output filename 2>")
    if (flag == "-c") :
        count_links(url, elem1, elem2)

    # -p http://cs111.byu.edu/Projects/project04/assets/data.html data.png data.csv"
    elif (flag == "-p") :
        plot_data(url, elem1, elem2)
    
   # -i http://cs111.byu.edu/Projects/project04/assets/images.html grey_ -g"
    elif (flag == "-i") :
        modify_img(url, elem1, elem2)
    
       

#________defensive coding that validates sys flags and arguments. 
def test_flags(argv):

    if len(argv) > 3:
        flag = argv[1]
        second_flag = argv[4]
        
        if (flag == "-c") :   
            return True
        
        elif (flag == "-p") :  
            return True
    
        elif (flag == "-i") :  
            if second_flag in ("-s", "-m", "-g", "-f"):
                return True
    return False
    



if __name__ == "__main__":
    """
    -p http://cs111.byu.edu/Projects/project04/assets/data.html data.png data.csv"
    -i http://cs111.byu.edu/Projects/project04/assets/images.html grey_ -g"
    -c <url> <output filename 1> <output filename 2>")

    """
    if (test_flags(sys.argv)) :
        main(sys.argv)
    else:
        print("\nInvalid arguments")








